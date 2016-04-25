import utils, texttab

from time import sleep
from random import randint

def nightly_sales_by_server(label=False, lag_days=1):

  tax_rate = texttab.TAXRATE

  return utils.select('''
    select sales.*, rbs.cc1, rbs.cc2, rbs.cash1, rbs.cash2, rbs.id as receipts_id
    from
    (
    SELECT 
      concat(p.last_name, ', ', substr(p.first_name,1,1), '.') server,
      p.id as person_id,
      p.ccid,
      sum(oi.price) sales, 
      sum(ti.price) taxable_sales,
      sum(oi.price) + COALESCE(round(sum(ti.price) * %(tax_rate)s, 2),0) receipts,
      count(distinct og.id) tabs_closed,
      convert(date(now() - INTERVAL '%(lag_days)s' DAY), CHAR(10)) as dat
    FROM (order_item oi left outer join taxable_item ti on ti.id = oi.id), order_group og, person p 
    WHERE oi.order_group_id = og.id 
    AND oi.is_cancelled = False
    AND oi.is_comped = False
    AND og.closedby = p.id 
    AND date(og.updated - interval '6' HOUR) = date(now() - INTERVAL '%(lag_days)s' DAY)
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
	SELECT concat(p.last_name, ', ', substr(p.first_name,1,1), '.') server,
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

def weekly_pay(printmode=0, incursor = None):

  if incursor is None:
    incursor = utils.get_cursor()

  for table_name in ('PAY_STUB', 'PAY_STUB_TEMP'):
    utils.execute('''
      create temporary table v_%(table_name)s
      as
      select
      week_of,
      last_name, first_name,
      hours_worked,
      pay_rate,
      fed_withholding + nys_withholding + medicare_tax + social_security_tax as weekly_tax,
      round(weekly_pay -fed_withholding -nys_withholding -medicare_tax -social_security_tax) as net_wage,
      tips,
      total_hourly_pay
      from %(table_name)s
      where yearweek(week_of) = yearweek(now() - interval '1' week)
      order by last_name, first_name''' % locals(),
      incursor=incursor,
      )

    if printmode == 1:
      break

  if printmode == 1:
    return utils.select('''select * from v_PAY_STUB''', incursor=incursor)
  else: 
    return utils.select('''
      select 
        pst.week_of,
        pst.last_name,
        pst.first_name,
        IF(pst.hours_worked = ps.hours_worked or ps.hours_worked is null,
          pst.hours_worked, concat(pst.hours_worked, ' / ', ps.hours_worked)) hours_worked,
        IF(pst.pay_rate = ps.pay_rate or ps.pay_rate is null, 
          pst.pay_rate, concat(pst.pay_rate, ' / ', ps.pay_rate)) pay_rate,
        IF(pst.weekly_tax = ps.weekly_tax or ps.weekly_tax is null, 
          pst.weekly_tax, concat(pst.weekly_tax, ' / ', ps.weekly_tax)) weekly_tax,
        IF(pst.net_wage = ps.net_wage or ps.net_wage is null, 
          pst.net_wage, concat(pst.net_wage, ' / ', ps.net_wage)) net_wage,
        IF(pst.tips = ps.tips or ps.tips is null, 
          pst.tips, concat(pst.tips, ' / ', ps.tips)) tips,
        IF(pst.total_hourly_pay = ps.total_hourly_pay or ps.total_hourly_pay is null, 
          pst.total_hourly_pay, concat(pst.total_hourly_pay, ' / ', ps.total_hourly_pay)) total_hourly_pay
        from   
        v_PAY_STUB_TEMP pst LEFT OUTER JOIN v_PAY_STUB ps on pst.week_of = ps.week_of
        and pst.first_name = ps.first_name and pst.last_name = ps.last_name
        order by last_name, first_name
    ''', 
    incursor = incursor,
    label= False
    )    

  
def get_active_items(incursor=None):

  return utils.select(
  ''' SELECT 
      oi.item_name as item_name, 
      og.table_id, 
      oi.id, oi.is_delivered, oi.is_held, oi.is_comped, oi.price,
      TIMESTAMPDIFF(MINUTE, oi.created, now()) minutes_old,
      TIMESTAMPDIFF(MINUTE, oi.updated, now()) minutes_since_mod,
      TIMESTAMPDIFF(SECOND, oi.updated, now()) seconds_since_mod,
      oi.is_cancelled,
      oi.parent_item
    FROM order_group og join order_item oi 
      on og.id = oi.order_group_id left outer join order_item oip 
      on oi.parent_item = oip.id
    where og.is_open = TRUE
    and (oi.is_cancelled = FALSE or TIMESTAMPDIFF(MINUTE, oi.updated, now()) < 1)
    order by oi.is_held, coalesce(oip.created, oi.created), oi.id'''
    , incursor)


  


  
