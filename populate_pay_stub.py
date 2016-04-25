import utils
import tax
from mylog import my_logger

def populate_pay_stub(temp = True, incursor=None):

  #days_of_tips_calculated = utils.select(
  #  '''select count(distinct date(intime)) from hours 
  #  where yearweek(intime) = yearweek(now() - interval '1' week) and tip_pay is not null''',
  #  label = False
  #  )[0][0]
  #if days_of_tips_calculated != 7:
  #  return 'Tips have been calculated for only %s days last week. When all days tips are calculated, refresh this page to see and print weekly pay for last week.'%days_of_tips_calculated

  results = utils.select('''
  select
  DATE(intime) - interval (DAYOFWEEK(intime) -1) DAY as week_of,
  hours_worked.person_id,
  last_name, first_name,
  sum(hours_worked) as hours_worked,
  pay_rate, 
  COALESCE(allowances, 0) allowances,
  COALESCE(nominal_scale, 0) nominal_scale,
  COALESCE(married, 0) married,
  COALESCE(salary, round(sum(hours_worked)*pay_rate)) as weekly_pay,
  COALESCE(salary, round(sum(hours_worked)*pay_rate)) * COALESCE(nominal_scale,0) as gross_wages,
  COALESCE(sum(tip_pay),0) tips,
  COALESCE(sum(tip_pay) / sum(hours_worked) + pay_rate, 0) as total_hourly_pay
  from hours_worked LEFT OUTER JOIN employee_tax_info ON hours_worked.person_id = employee_tax_info.person_id
  #where yearweek(intime) = yearweek(now() - interval '1' week)
  #and intime != 0
  where intime != 0
  and year(intime) = 2016
  group by hours_worked.person_id, yearweek(intime)
  ''',
  incursor = incursor,
  label = True
  )

  if temp:
    utils.execute('''
    create temporary table PAY_STUB_TEMP like PAY_STUB;
    ''', incursor=incursor);
    table_names = ('PAY_STUB_TEMP',)
  else:
    table_names = ('PAY_STUB', 'WEEKLY_PAY_STUB')

  for row in results:
    if not temp and utils.select(
      'select 1 from PAY_STUB where week_of = "%(week_of)s" and person_id = %(person_id)s'%row,
      incursor = incursor
      ):
      continue

    for table_name in table_names:
      if table_name == 'WEEKLY_PAY_STUB':
        row['gross_wages'] = row['weekly_pay'] + float(row['tips'])
        row['pay_rate'] = round(row['total_hourly_pay'])

      tax.add_witholding_fields(row)
      columns = ', '.join(row.keys())
      values = ', '.join(("'%s'" % value for value in row.values()))
      sqltext = 'INSERT into %s (%s) VALUES (%s);'%(table_name, columns, values)
      my_logger.debug('pay stub: ' + sqltext)
      utils.execute(sqltext, incursor=incursor)
    

if __name__ == '__main__':

  populate_pay_stub(temp=False)

