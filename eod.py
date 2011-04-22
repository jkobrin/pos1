
import json
import MySQLdb
import utils



def index(req):

  results = utils.select('''
    SELECT 
      p.last_name server, 
      sum(price) collected, 
      count(distinct og.id) tabs_closed
    FROM order_item oi, order_group og, person p 
    WHERE oi.order_group_id = og.id 
    AND oi.is_cancelled = False
    AND og.closedby = p.id 
    AND og.created > now() - INTERVAL '12' HOUR
    GROUP BY p.id, p.last_name;''',
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
    '''</body></html>'''
  )

  return html

if __name__ == '__main__':
  print 'hi'
