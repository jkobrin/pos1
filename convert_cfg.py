
import yaml, json
from mylog import my_logger
import utils
from texttab import TAXRATE
log = my_logger

CONFIG_FILE_NAME = '/var/www/' + utils.hostname() + '_config_old.yml'

MAX_NAME_LEN = 32

def config_insert():
  cfg = yaml.load(open(CONFIG_FILE_NAME))
  for category in cfg['menu']['categories']:
    catname = category['name']
    if catname in ('tables',):
      continue
    for subcat in category['subcategories']:
      if subcat in ('spirits', 'shots'):
        continue
      subcatname = subcat['name']
      for item in subcat['items']:
        if not item.has_key('name'):
           raise Exception('no name for item: ' + str(item))
        item['name'] = unicode(item['name'])[:MAX_NAME_LEN]
        dct = {
        'name' : item['name'],
        'supercategory' : catname,
        'category' : subcatname,
        'subcategory' : '',
        'retail_price' : item.get('price') or item.get('add_on_price'),
        'add_on' : item.has_key('add_on_price'),
        'qtprice' : '',
        'scalable' : item.has_key('scale_units'),
        'tax' : subcat.get('tax'),
        'wholesale_price' : item.get('wholesale'),
        'supplier' : item.get('supplier'),
        'vendor_code' : item.get('vendor_code'),
        'bin' : 1,
        'listorder' : 0,
        'upc' : item.get('upc'),
        'description' : None,
        'active' : True,
        'units_in_stock' : None,
        'inventory_date' : None,
        'mynotes' : None
        }

        utils.sql_insert('sku', dct)


def wine_insert():  
  winelist = utils.select('''select * from winelist order by id''')

  for item in winelist:
    if item['grapes']:
      item['grapes'] = 'Grapes: %s'%item['grapes']
    dct = {
    'id' : item['id'],
    'name' : item['name'],
    'supercategory' : 'bev',
    'category' : item['category'],
    'subcategory' : item['subcategory'],
    'retail_price' : item['listprice'],
    'qtprice' : item['qtprice'],
    'scalable' : False,
    'tax' : 'standard',
    'wholesale_price' : item['frontprice'],
    'supplier' : item['supplier'],
    'vendor_code' : None,
    'bin' : item['bin'],
    'listorder' : item['listorder'],
    'upc' : None,
    'description' : '\n'.join((i for i in (item['byline'], item['grapes'], item['notes']) if i)),
    'active' : item['active'],
    'units_in_stock' : item['units_in_stock'],
    'inventory_date' : item['inventory_date'],
    'mynotes' : item['mynotes']
    }

    utils.sql_insert('sku', dct)

#wine_insert()  
config_insert()  
