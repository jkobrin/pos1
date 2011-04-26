import utils

def nightly_sales_by_server(label=False):

  return utils.select('''
    SELECT 
      p.last_name server, 
      sum(price) sales, 
      count(distinct og.id) tabs_closed
    FROM order_item oi, order_group og, person p 
    WHERE oi.order_group_id = og.id 
    AND oi.is_cancelled = False
    AND og.closedby = p.id 
    AND og.created > now() - INTERVAL '48' HOUR
    GROUP BY p.id, p.last_name;''',
    incursor=None,
    label=label
  )
