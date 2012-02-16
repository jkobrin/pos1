import utils

def nightly_sales_by_server(label=False, lag_hours=16):

  return utils.select('''
    SELECT 
      p.last_name server, 
      sum(oi.price) sales, 
      sum(ri.price) taxable_sales,
      count(distinct og.id) tabs_closed
    FROM (order_item oi left join revenue_item ri on ri.id = oi.id), order_group og, person p 
    WHERE oi.order_group_id = og.id 
    AND oi.is_cancelled = False
    AND oi.is_comped = False
    AND og.closedby = p.id 
    AND date(oi.created - interval '6' HOUR) = date(now() - INTERVAL '%(lag_hours)s' HOUR)
    GROUP BY p.id, p.last_name;''' % locals(),
    incursor=None,
    label=label
  )

