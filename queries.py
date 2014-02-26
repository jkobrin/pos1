import utils, texttab


def nightly_sales_by_server(label=False, lag_days=1):

  tax_rate = texttab.TAXRATE

  return utils.select('''
    select sales.*, rbs.cc1, rbs.cc2, rbs.cash1, rbs.cash2, rbs.id as receipts_id
    from
    (
    SELECT 
      p.last_name server, 
      p.id as person_id,
      p.ccid,
      sum(oi.price) sales, 
      sum(ri.price) taxable_sales,
      sum(oi.price) + COALESCE(round(sum(ri.price) * %(tax_rate)s, 2),0) receipts,
      count(distinct og.id) tabs_closed,
      convert(date(now() - INTERVAL '%(lag_days)s' DAY), CHAR(10)) as dat
    FROM (order_item oi left outer join revenue_item ri on ri.id = oi.id), order_group og, person p 
    WHERE oi.order_group_id = og.id 
    AND oi.is_cancelled = False
    AND oi.is_comped = False
    AND og.closedby = p.id 
    AND date(oi.created - interval '6' HOUR) = date(now() - INTERVAL '%(lag_days)s' DAY)
    GROUP BY p.id) sales
    left outer join
    (select *
    from receipts_by_server
    where dat = date(now() - INTERVAL '%(lag_days)s' DAY)
    ) rbs on sales.person_id = rbs.person_id ;''' % locals(),
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

def weekly_pay(printmode=0):
 return utils.select('''
	select
	DATE(intime) - interval (DAYOFWEEK(intime) -1) DAY as week_of,
	last_name, first_name,
	sum(hours_worked) as hours_worked,
  pay_rate, 
  weekly_tax,
  round(sum(hours_worked)*pay_rate - weekly_tax) as weekly_pay,
  sum(tip_pay) tips,
  round(sum(hours_worked)*pay_rate - weekly_tax) + sum(tip_pay) as total_weekly,
  sum(tip_pay) / sum(hours_worked) + pay_rate as total_hourly_pay
	from hours_worked 
  where (yearweek(intime) > yearweek(now() - interval '5' week) and %(printmode)s = 0)
     or (yearweek(intime) = yearweek(now() - interval '1' week) and %(printmode)s = 1)
     and intime != 0
  group by yearweek(intime), last_name 
	order by yearweek(intime) desc, last_name''' % locals(),
    incursor=None,
    label=printmode
  )


