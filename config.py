

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

  for category in raw_winelist:
    raw_catname = category['name']
    raw_items = category['items']
    subcat = {'name': raw_catname, 'items': []}
    wine_category['subcategories'].append(subcat)
    for raw_item in raw_items:
      log.debug('Parsing winelist item: ' + str(raw_item))
      try:
        bin_num = raw_item.get('bin')
        if not bin_num: continue
        name = '%s %s' % (bin_num, raw_item['name'])

        listprice = raw_item.get('listprice')
        if not listprice : continue

        # make regular item
        item = {
          'name' : name,
          'price' : listprice
        }  
        subcat['items'].append(item)

        # now make quartino
        if item.has_key('qtprice'):
          price = item['qtprice']
        else:
          price = float(listprice) / 4 + 2
        qtitem = {
          'name' : '%s %s'%(bin_num, 'qtino'),
          'price' : price
        }  
        subcat['items'].append(qtitem)

      except KeyError as ke:
        log.error('Key error:' + ke.message)
  

  cfg['menu']['categories'].append(wine_category)
