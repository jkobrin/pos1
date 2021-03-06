import sys


import json
import MySQLdb
import utils

from config import expand_extra_fields


def index(req):
  
  bev_sold = utils.select('''
  SELECT item_name, count(*), sku.category, group_concat(TIME_FORMAT(order_item.created, '%H:%i'))
  FROM order_item join sku on order_item.menu_item_id = sku.id
  WHERE date(order_item.created - INTERVAL '4' hour) = date(now() - INTERVAL '28' hour)
  and order_item.is_cancelled = False
  and sku.supercategory rlike 'wine|bar'
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
      "Yesterday wine & bar sales",
      ('Name','Count', 'Category', 'Order Times'), 
      bev_sold
    )
  )

  bev_week_sold = utils.select('''
  SELECT item_name, count(*), sku.category, group_concat(order_item.created)
  FROM order_item join sku on order_item.menu_item_id = sku.id
  WHERE yearweek(order_item.created - INTERVAL '4' hour) = yearweek(now() - INTERVAL '28' hour)
  and order_item.is_cancelled = False
  and sku.supercategory rlike 'wine|bar'
  group by item_name
  order by sku.category, item_name;''',
  incursor=None,
  label=False
  )

  week_eod = utils.select('''
    SELECT sum(total), sum(dtotal)  
    FROM nd_tots  
    WHERE dat > date(now() - INTERVAL '1' week);''' % locals(),
    incursor=None,
    label=False
  )
  
  html += (
    utils.tohtml(
    "Week Totals",
    ('Dinner','Lunch'), 
    week_eod
    )  +
    utils.tohtml(
      "Week wine & bar sales",
      ('Name','Count', 'Category', 'Order Times'), 
      bev_week_sold
    )
  )

  winebar = utils.select('''
    SELECT supplier, category, name, estimated_units_remaining as eur, extra
    FROM sku_inv
    WHERE onpos = true
    order by supplier
  ''',
  incursor=None,
  label=True
  )
  
  par_alerts = []
  for item in winebar:
    expand_extra_fields(item)

    if item.has_key('par') and int(item['eur']) <= item['par']:
      par_alerts.append((item['supplier'], item['category'], item['name'], item['eur'], item['par']))


  html += (
    utils.tohtml(
    "Par Alerts",
    ('supplier', 'category', 'name', 'estimated_units_remaining', 'par'),
    par_alerts
    ) +
    '''</body></html>'''
  )

  return html



if __name__ == '__main__':
  print 'hi'
