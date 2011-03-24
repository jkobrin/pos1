

import yaml, json
import mylog
log = mylog.my_logger

CONFIG_FILE_NAME = '/var/www/config.yml'
WINELIST_FILE_NAME = '/var/www/winelist.yml'


def get():
  cfg = yaml.load(open(CONFIG_FILE_NAME))
  populate_wine_category(cfg)  
  return json.dumps(cfg)


def populate_wine_category(cfg):

  # find the list data structure that is to hold the wines
  #for category in cfg['menu']:
  #  if category['name'] = 'wine':
  #    winelist = category['items']
  #    break
  wine_category = {'name': 'wine', 'subcategories': []}

  raw_winelist = yaml.load(open(WINELIST_FILE_NAME))

  bin_num = 0
  for raw_catname, raw_items in raw_winelist.items():
    subcat = {'name': raw_catname, 'items': []}
    qtsubcat = {'name': raw_catname + ' by quartino', 'items': []}
    wine_category['subcategories'].append(subcat)
    wine_category['subcategories'].append(qtsubcat)
    for raw_item in raw_items:
      log.debug('Parsing winelist item: ' + str(raw_item))
      try:
        bin_num += 1
        name = '%s %s' % (bin_num, raw_item['name'])

        # make regular item
        item = {
          'name' : name,
          'price' : raw_item['listprice']
        }  
        subcat['items'].append(item)

        # now make quartino
        if item.has_key('qtprice'):
          price = item['qtprice']
        else:
          price = float(raw_item['listprice']) / 4 + 2
        qtitem = {
          'name' : name,
          'price' : price
        }  
        qtsubcat['items'].append(qtitem)

      except KeyError as ke:
        log.error('Key error:' + ke.message)
  

  cfg['menu']['categories'].append(wine_category)
