import utils
import tax
from mylog import my_logger


def index(req = None): #for simple viewing convenience
  return '\n\n'.join('{first_name} {last_name}: {weekly_pay}/{gross_wages} tips:{tips}'.format(**row) for row in get_pay())
    

def get_pay(incursor=None):

  return utils.select('''
  select
  DATE(now() - interval '1' week) - interval (DAYOFWEEK(now() - interval '1' week) -1) DAY as week_of, #sunday last week
  person.id as person_id,
  person.last_name, person.first_name,
  sum(hours_worked) as hours_worked,
  person.pay_rate, 
  COALESCE(allowances, 0) allowances,
  COALESCE(nominal_scale, 0) nominal_scale,
  COALESCE(married, 0) married,
  COALESCE(person.salary, 0) + COALESCE(round(sum(hours_worked)*person.pay_rate), 0) as weekly_pay,
  COALESCE(person.salary* COALESCE(nominal_scale,0), 0) + COALESCE(round(sum(hours_worked)*person.pay_rate), 0) * COALESCE(nominal_scale,0) as gross_wages,
  COALESCE(sum(tip_pay),0) tips,
  COALESCE(sum(tip_pay) / sum(hours_worked), 0)+person.pay_rate as total_hourly_pay
  FROM 
    person
  LEFT OUTER JOIN
    (select * from hours_worked 
    where yearweek(intime) = yearweek(now() - interval '1' week)
    and intime != 0) hours_worked 
  ON person.id = hours_worked.person_id
  LEFT OUTER JOIN employee_tax_info 
  ON person.id = employee_tax_info.person_id
  where person.salary > 0 or hours_worked.hours_worked > 0
  group by person.id, yearweek(intime)
  ''',
  incursor = incursor,
  label = True
  )


def populate_pay_stub(temp = True, incursor=None):

  #days_of_tips_calculated = utils.select(
  #  '''select count(distinct date(intime)) from hours 
  #  where yearweek(intime) = yearweek(now() - interval '1' week) and tip_pay is not null''',
  #  label = False
  #  )[0][0]
  #if days_of_tips_calculated != 7:
  #  return 'Tips have been calculated for only %s days last week. When all days tips are calculated, refresh this page to see and print weekly pay for last week.'%days_of_tips_calculated

  if temp:
    utils.execute('''
    create temporary table PAY_STUB_TEMP like PAY_STUB;
    ''', incursor=incursor);
    table_names = ('PAY_STUB_TEMP',)
  else:
    table_names = ('PAY_STUB', 'WEEKLY_PAY_STUB')

  for row in get_pay():
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
      utils.sql_insert(table_name, row, incursor)


if __name__ == '__main__':

  populate_pay_stub(temp=False)

