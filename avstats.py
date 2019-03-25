import sys


import json
import MySQLdb
import utils



def index(req):
  
  bev_sold = utils.select('''
  SELECT item_name, count(*), sku.category, group_concat(TIME_FORMAT(order_item.created, '%H:%i'))
  FROM order_item join sku on order_item.menu_item_id = sku.id
  WHERE date(order_item.created - INTERVAL '4' hour) = date(now() - INTERVAL '28' hour)
  and order_item.is_cancelled = False
  and sku.supercategory = 'bev'
  group by item_name
  order by sku.category, item_name;''',
  incursor=None,
  label=False
  )

  eod = utils.select('''
    SELECT total, dtotal  
    FROM nd_tots  
    WHERE dat = date(now() - INTERVAL '1' day);''' % locals(),
    incursor=None,
    label=False
  )
  
  html = (
    '''  
      <html>
      <body>
    ''' + 
    utils.tohtml(
    "Totals",
    ('Dinner','Lunch'), 
    eod
    )  +
    utils.tohtml(
      "Yesterday BEV sales",
      ('Name','Count', 'Category', 'Order Times'), 
      bev_sold
    ) +
    '''</body></html>'''  
  )

  return html




if __name__ == '__main__':
  print 'hi'
