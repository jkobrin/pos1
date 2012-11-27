import utils, texttab


def nightly_sales_by_server(label=False, lag_days=1):

  tax_rate = texttab.TAXRATE

  return utils.select('''
    SELECT 
      p.last_name server, 
      p.ccid,
      sum(oi.price) sales, 
      sum(ri.price) taxable_sales,
      sum(oi.price) + round(sum(ri.price) * %(tax_rate)s, 2) receipts,
      count(distinct og.id) tabs_closed
    FROM (order_item oi left join revenue_item ri on ri.id = oi.id), order_group og, person p 
    WHERE oi.order_group_id = og.id 
    AND oi.is_cancelled = False
    AND oi.is_comped = False
    AND og.closedby = p.id 
    AND date(oi.created - interval '6' HOUR) = date(now() - INTERVAL '%(lag_days)s' DAY)
    GROUP BY p.id, p.last_name;''' % locals(),
    incursor=None,
    label=label
  )

def hours(lag_days):

  return utils.select('''
	SELECT p.last_name,
	h.id, 
  convert(intime, CHAR(48)) intime,
  convert(outtime, CHAR(48)) outtime,
  convert(tip_share, CHAR(4)) tip_share,
  convert(tip_pay, CHAR(3)) tip_pay
	from hours h, person p
  where date(intime) = date(now() - INTERVAL '%(lag_days)s' DAY)
  and h.person_id = p.id
	order by intime;'''%locals(),
    incursor=None,
    label=True
  )
