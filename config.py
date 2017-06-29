
import yaml, json, re
from mylog import my_logger
import utils
from texttab import TAXRATE
log = my_logger

CONFIG_FILE_NAME = '/var/www/' + utils.hostname() + '_config.yml'

MAX_NAME_LEN = 32

winecats = re.compile('.* Wine|Before \& After|Dessert|Bubbly')

def load_config():
  cfg = yaml.load(open(CONFIG_FILE_NAME))

  populate_staff_tabs(cfg)
  load_db_config(cfg)  

  for category in cfg['menu']['categories']:
    catname = category['name']
    for subcat in category['subcategories']:
      subcatname = subcat['name']
      for item in subcat['items']:
        item['category'] = catname
        item['subcategory'] = subcatname
        item['price'] = item.get('retail_price')
        if not item.has_key('name'):
           raise Exception('no name for item: ' + str(item))
        item['name'] = unicode(item['name'])[:MAX_NAME_LEN]
        if 'included' in (subcat.get('tax'), item.get('tax'))  and item.get('price'):
          item['price'] /= (1 + TAXRATE) # remove the tax from price

  return cfg

def get():  
  cfg = load_config()
  return json.dumps(cfg, cls=utils.MyJSONEncoder)


def load_db_config(cfg):
  
  supercats = utils.select('''select distinct supercategory as name from sku''')
  for supercat in supercats:
    cfg['menu']['categories'].append(supercat)
    supercat['subcategories'] = []
    for cat in utils.select('''select distinct category as name from sku where supercategory = %s 
      and bin is not null and active=True''', 
        args = (supercat['name'])):
      supercat['subcategories'].append(cat)
      cat['items'] = []
      for item in utils.select('''select * from sku where supercategory = %s and category = %s
      and bin is not null and active=True
      order by bin''', args = (supercat['name'], cat['name'])):
        cat['items'].append(item)
        if winecats.match(cat['name']):
          item['name'] = item['bin'] + ' ' + item['name']
          my_logger.info('name: modified ' + item['name'])
          if item['qtprice'] > 0: 
            my_logger.info('qt: added ' + item['name'])
            qtitem = item.copy()
            qtitem['fraction'] = .25
            qtitem['retail_price'] = item['qtprice']
            qtitem['name'] = 'qt: '+item['name']
            cat['items'].append(qtitem)


def populate_staff_tabs(cfg):

    items = utils.select('''
      select concat(first_name, ' ', last_name) as name
      from person
      ''')
    table_cat_results = [cat for cat in cfg['menu']['categories'] if cat['name'] == 'tables']
    if len(table_cat_results) != 1: raise Exception('Problem finding tables category')
    table_category = table_cat_results[0]
    staff_subcat = {'name': 'staff_tabs', 'items': items}
    table_category['subcategories'].append(staff_subcat)



if __name__ == '__main__':
  print load_db_config()
