
import json
import MySQLdb
import utils



def index(req):

  results = utils.select('''
    SELECT 
	item_name, count(*) count, DATE(created)
	from order_item where is_cancelled = false 
	group by item_name, date(created)
	order by date(created), item_name
  ''',
    incursor=None,
    label=False
  )

  
  html = (
    '''  
      <html>
      <body>
    ''' + 
    utils.tohtml(
      'items sold',
      ('name', 'count', 'date'), 
      results
    ) +
    '''</body></html>'''
  )

  return html

if __name__ == '__main__':
  print 'hi'
