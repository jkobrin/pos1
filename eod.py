
import json
import MySQLdb
import utils
import queries


def index(req):

  results = queries.nightly_sales_by_server()

  seven_day_total = utils.select('''
    SELECT sum(price) total  
    FROM order_item oi, order_group og, person p 
    WHERE oi.order_group_id = og.id 
    AND og.closedby = p.id
    and oi.is_cancelled = false
    AND oi.created > now() - INTERVAL '7' DAY;''',
    incursor=None,
    label=False
  )
  
  grand_total = utils.select('''
    SELECT sum(price) total  
    FROM order_item oi, order_group og, person p 
    WHERE oi.order_group_id = og.id 
    AND og.closedby = p.id
    and oi.is_cancelled = false
    AND oi.created > now() - INTERVAL '12' HOUR;''',
    incursor=None,
    label=False
  )
  
  html = (
    '''  
      <html>
      <body>
    ''' + 
    utils.tohtml(
      'Nightly Receipts by Server',
      ('Server', 'Receipts', 'Tabs Closed'), 
      results
    ) +
    utils.tohtml(
      "Nightly Total",
      ('Total',), 
      grand_total
    ) +

    utils.tohtml(
      "7 day Total",
      ('Total',), 
      seven_day_total
    ) +
    '''</body></html>'''
  )

  return html

if __name__ == '__main__':
  print 'hi'
