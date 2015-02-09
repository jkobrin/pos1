import utils
import tax
from mylog import my_logger

def populate_pay_stub():

  results = utils.select('''
  select
  DATE(intime) - interval (DAYOFWEEK(intime) -1) DAY as week_of,
  hours_worked.person_id,
  last_name, first_name,
  sum(hours_worked) as hours_worked,
  pay_rate, 
  IFNULL(allowances, 0) allowances,
  IFNULL(nominal_scale, 0) nominal_scale,
  IFNULL(married, 0) married,
  round(sum(hours_worked)*pay_rate) as weekly_pay,
  round(sum(hours_worked)*pay_rate*IFNULL(nominal_scale,0)) as gross_wages,
  sum(tip_pay) tips,
  sum(tip_pay) / sum(hours_worked) + pay_rate as total_hourly_pay
  from hours_worked LEFT OUTER JOIN employee_tax_info ON hours_worked.person_id = employee_tax_info.person_id
  where yearweek(intime) = yearweek(now() - interval '1' week)
  and intime != 0
  group by hours_worked.person_id
  ''',
  incursor = None,
  label = True
  )

  for row in results:
    tax.add_witholding_fields(row)
    columns = ', '.join(row.keys())
    values = ', '.join(("'%s'" % value for value in row.values()))
    sqltext = 'INSERT into PAY_STUB (%s) VALUES (%s);'%(columns, values)
    my_logger.debug('pay stub: ' + sqltext)
    utils.execute(sqltext)
    

if __name__ == '__main__':

  populate_pay_stub()

