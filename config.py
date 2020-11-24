import json, re, copy, yaml
from mylog import my_logger
import utils
import config_loader
import whiteboard

log = my_logger

MAX_NAME_LEN = 32
BTG_NAME = "by the glass"
ALLWINE_NAME = 'wine by bin'

TAXRATE = .08625


def expand_extra_fields(item):
  if item.get('extra'):
    try:
      item.update(yaml.load(item['extra']))
    except ValueError as e:
      log.warn(e.message + ' when parsing: %s'%item)
      


def load_config():
  cfg = copy.deepcopy(config_loader.get_config_dict())

  populate_staff_tabs(cfg)
  load_db_config(cfg)  

  for supercategory in cfg['menu']['supercategories']:
    supercatname = supercategory['name']
    for cat in supercategory['categories']:
      catname = cat['name']
      for item in cat['items']:
        expand_extra_fields(item)
        item['supercategory'] = supercatname
        item['category'] = catname
        item['price'] = item.get('retail_price')

        if not item.has_key('name'):
           raise Exception('no name for item: ' + str(item))
        item['name'] = unicode(item['name'])[:MAX_NAME_LEN]
        if 'included' in (cat.get('tax'), item.get('tax'))  and item.get('price'):
          item['price'] /= (1 + TAXRATE) # remove the tax from price

  return cfg

def get():  
  cfg = load_config()
  return json.dumps(cfg, cls=utils.MyJSONEncoder)


def load_db_config(cfg):
  
  supercats = utils.select('''
    select supercategory as name, onmenu, onpos, description
    from sku
    where category='HEAD' and name = 'HEAD' 
    and (onpos = true or onmenu = true)
    order by listorder''') 

  for supercat in supercats:
    cfg['menu']['supercategories'].append(supercat)
    supercat['categories'] = []

    if supercat['name'] == 'wine':
      scalable = utils.select('''
        select distinct id from sku where scalable = true and supercategory = %s and name != 'HEAD' ''',
        args=[supercat['name']])
      scalables = [rec["id"] for rec in scalable]

      allwine = {'name':ALLWINE_NAME, 'onmenu': False, 'onpos': True, 'items': []}
      btg = {'name':BTG_NAME, 'onmenu': True, 'onpos': True, 'items': []}
      supercat['categories'].append(btg)

    cats = utils.select('''
      select category as name, onmenu, onpos, description
      from sku 
      where (onmenu = true or onpos=true)
      and supercategory = %s and category != 'HEAD' and name = 'HEAD'
      order by ifnull(listorder, ~0)''',
      # ~0 (bitwise neg of 0) is MAX_INT so as to put non-list items last
      args=[supercat['name']])

    for cat in cats:
      supercat['categories'].append(cat)
      cat['items'] = []
      for item in utils.select('''
      select * from sku 
      where supercategory = %s and category = %s
      and (onmenu = true or onpos = true) and name != 'HEAD'
      order by ifnull(listorder, ~0), name''', args = (supercat['name'], cat['name'])):

        cat['items'].append(item)
        #make quartino items
        if supercat['name'] == 'wine':
          item['display_name'] = item['display_name'] or item['name'] 
          item['name'] = str(item['bin']) + ' ' + str(item['name'])
          allwine_item = item.copy()
          allwine_item['subcategory'] = 'bottle'
          allwine['items'].append(allwine_item)

          if item['qtprice'] > 0: 
            qtitem = item.copy()
            qtitem['subcategory'] = cat['name']
            qtitem['fraction'] = .25
            qtitem['is_glass'] = True
            qtitem['bottle_price'] = item['retail_price']
            qtitem['retail_price'] = item['qtprice']
            qtitem['name'] = 'qt: '+item['name']
            allwine_qtitem = qtitem.copy()
            allwine_qtitem['subcategory'] = 'quartino'
            allwine['items'].append(allwine_qtitem)
            if qtitem['id'] in scalables:
              btg['items'].append(qtitem)
          elif item['id'] in scalables:     
            btg['items'].append(item)
            
    #this has to be down here cause I want allwine to be the last thing in the supercategory
    if supercat['name'] == 'wine':
      allwine['items'].sort(key=lambda wine: wine['subcategory'] + ':' + wine['bin'])
      supercat['categories'].append(allwine)

  cfg['whiteboard_content'] = whiteboard.get_content()



def populate_staff_tabs(cfg):

    items = utils.select('''
      select concat(first_name, ' ', last_name) as name
      from person
      ''')
    table_supercat_results = [cat for cat in cfg['menu']['supercategories'] if cat['name'] == 'tables']
    if len(table_supercat_results) != 1: raise Exception('Problem finding tables supercategory')
    table_supercategory = table_supercat_results[0]
    staff_cat = {'name': 'staff_tabs', 'items': items}
    table_supercategory['categories'].append(staff_cat)



if __name__ == '__main__':
  cfg= load_config()
  for supercat in cfg['menu']['supercategories']:
    if supercat['name'] == 'tables':
      continue

    print (supercat['name'], supercat['listorder'])
      
