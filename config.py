
import json, re, copy
from mylog import my_logger
import utils
import config_loader
from texttab import TAXRATE
log = my_logger

MAX_NAME_LEN = 32
winecats = re.compile('^red$|^white|^bubbly')

def load_config():
  cfg = copy.deepcopy(config_loader.config_dict)

  populate_staff_tabs(cfg)
  load_db_config(cfg)  

  for supercategory in cfg['menu']['supercategories']:
    supercatname = supercategory['name']
    for cat in supercategory['categories']:
      catname = cat['name']
      for item in cat['items']:
        item['supercategory'] = supercatname
        item['category'] = catname
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
  
  supercats = utils.select('''
    select supercategory as name from sku 
    where active = true and bin is not null 
    group by supercategory order by min(if(listorder>0, listorder, null ))''')

  for supercat in supercats:
    cfg['menu']['supercategories'].append(supercat)
    supercat['subcategories'] = []

    if supercat['name'] == 'bev':
      scalable = utils.select('''
        select distinct id from sku where scalable = true and supercategory = 'bev' ''');
      scalables = [rec["id"] for rec in scalable]

      recent = utils.select('''select distinct menu_item_id from order_item 
        where item_name rlike 'qt:' and date(created) > curdate() - interval '72' hour''')
      recents = [rec["menu_item_id"] for rec in recent]

      btg = {'name':"by_the_glass", 'items': []}
      supercat['subcategories'].append(btg)

    cats = utils.select('''
      select category as name from sku 
      where active = true and bin is not null 
      and bin != '0' and active = True and category is not null
      and supercategory = %s
      group by category order by min(if(listorder>0, listorder, null ))''', args=[supercat['name']])

    for cat in cats:
      supercat['subcategories'].append(cat)
      cat['items'] = []
      for item in utils.select('''select * from sku where supercategory = %s and category = %s
      and bin is not null and bin != '0' and active=True
      order by listorder, bin, name''', args = (supercat['name'], cat['name'])):
        cat['items'].append(item)

        #make quartino items
        if winecats.search(cat['name']):
          item['name'] = item['bin'] + ' ' + item['name']
          my_logger.info('name: modified ' + item['name'])
          if item['qtprice'] > 0: 
            my_logger.info('qt: added ' + item['name'])
            qtitem = item.copy()
            qtitem['fraction'] = .25
            qtitem['retail_price'] = item['qtprice']
            qtitem['name'] = 'qt: '+item['name']
            cat['items'].append(qtitem)
            if qtitem['id'] in scalables:
              btg['items'].append(qtitem)


def populate_staff_tabs(cfg):

    items = utils.select('''
      select concat(first_name, ' ', last_name) as name
      from person
      ''')
    table_supercat_results = [cat for cat in cfg['menu']['supercategories'] if cat['name'] == 'tables']
    if len(table_supercat_results) != 1: raise Exception('Problem finding tables supercategory')
    table_supercategory = table_cat_results[0]
    staff_cat = {'name': 'staff_tabs', 'items': items}
    table_category['categories'].append(staff_cat)



if __name__ == '__main__':
  print load_db_config()
