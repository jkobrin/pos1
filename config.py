
import yaml, json
from mylog import my_logger
import utils
from texttab import TAXRATE
log = my_logger

CONFIG_FILE_NAME = '/var/www/' + utils.hostname() + '_config.yml'

MAX_NAME_LEN = 32

def iget():
  items = {}
  cfg = yaml.load(open(CONFIG_FILE_NAME))
  populate_wine_category(cfg)  
  populate_staff_tabs(cfg)

  for category in cfg['menu']['categories']:
    catname = category['name']
    for subcat in category['subcategories']:
      subcatname = subcat['name']
      for item in subcat['items']:
        item['catname'] = catname
        item['subcatname'] = subcatname
        if not item.has_key('name'):
           raise Exception('no name for item: ' + str(item))
        item['name'] = str(item['name'])[:MAX_NAME_LEN]
        if subcat.get('tax') == 'included' and item.get('price'):
          item['price'] /= (1 + TAXRATE) # remove the tax from price
        items[item['name']] = item
  return cfg, items

def get():  
  cfg, items = iget()
  return json.dumps(cfg)

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



def populate_wine_category(cfg):

  bev_category_results = [cat for cat in cfg['menu']['categories'] if cat['name'] == 'bev']
  if len(bev_category_results) != 1: raise Exception('Problem loading bev category')
  bev_category = bev_category_results[0]

  winecats = utils.select('''select distinct category from active_wine''')
  for cat in winecats:
    cat = cat['category']
    items = utils.select('''
      select id, bin, qtprice as price, CONCAT('qt: ', bin," ", name ) as name
      from winelist
      where category = '%(cat)s' and active = true and qtprice is not null and qtprice != 0 and bin is not null
      union all
      select id, bin, listprice as price, CONCAT(bin," ", name ) as name
      from winelist
      where category = '%(cat)s' and active = true and listprice != 0 and listprice is not null and bin is not null
      order by bin
      ''' % locals())
    bev_subcat = {'name': cat, 'items': items}
    bev_category['subcategories'].append(bev_subcat)


if __name__ == '__main__':
  cfg, items = iget()
  for it in items.items():
    print it
