

import yaml, json
from mylog import my_logger
log = my_logger

CONFIG_FILE_NAME = '/var/www/config.yml'
WINELIST_FILE_NAME = '/var/www/winelist.yml'


def get():
  cfg = yaml.load(open(CONFIG_FILE_NAME))
  populate_wine_category(cfg)  

  for category in cfg['menu']['categories']:
    catname = category['name']
    for subcat in category['subcategories']:
      subcatname = subcat['name']
      for item in subcat['items']:
        item['catname'] = catname
        item['subcatname'] = subcatname

  return json.dumps(cfg)


def populate_wine_category(cfg):

  # find the list data structure that is to hold the wines
  #for category in cfg['menu']:
  #  if category['name'] = 'wine':
  #    winelist = category['items']
  #    break
  bev_category = {'name': 'bev', 'subcategories': []}
  redcat = {'name': 'red wine', 'items': []}
  whitecat = {'name': 'white wine', 'items': []}
  othercat = {'name': 'bubbly, beer & other', 'items': []}

  for subcat in (redcat, whitecat, othercat):
    bev_category['subcategories'].append(subcat)

  raw_winelist = yaml.load(open(WINELIST_FILE_NAME))

  for category in raw_winelist:
    raw_catname = category['name']
    raw_items = category['items']
    if 'red' in raw_catname.lower():
      subcat = redcat
    elif 'white' in raw_catname.lower():
      subcat = whitecat
    else:
      subcat = othercat

    raw_items.sort(key = lambda i: str(i.get('bin')))
    for raw_item in raw_items:
      log.debug('Parsing winelist item: ' + str(raw_item))
      try:
        bin_num = raw_item.get('bin')
        if not bin_num: continue
        name = '%s %s' % (bin_num, raw_item['name'])

        listprice = raw_item.get('listprice')
        if listprice :
          # make regular item
          item = {
            'name' : name,
            'price' : listprice
          }  
          subcat['items'].append(item)

        # now make quartino
        if raw_item.has_key('qtprice'):
          price = raw_item['qtprice']
          qtitem = {
            'name' : 'qt: '+name,
            'price' : price
          }  
          subcat['items'].append(qtitem)

      except KeyError as ke:
        log.error('Key error:' + ke.message)
  

  cfg['menu']['categories'].append(bev_category)
