
import json
import MySQLdb
import utils
import config


def index(req, subcat=None):

  results = utils.select('''
    SELECT 
	item_name, count(*) count, DATE(created) dat
	from order_item 
  where is_cancelled = false 
	group by item_name, date(created)
	order by date(created) desc, item_name
  ''',
    incursor=None,
    label=False
  )
  if subcat:
    cfg, cfg_items = config.iget()
    filtered_items = []
    for res in results:
      name, count, dat = res
      item = cfg_items.get(name)
      if item and item['subcatname'] == subcat:
        filtered_items.append(res)
  else:
    filtered_items = results
  
  html = (
    '''  
      <html>
      <body>
    ''' + 
    utils.tohtml(
      'items sold',
      ('name', 'count', 'date'), 
      filtered_items
    ) +
    '''</body></html>'''
  )

  return html

if __name__ == '__main__':
  print 'hi'
