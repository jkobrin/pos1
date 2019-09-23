import sys
import json
import MySQLdb
import utils, queries, print_pay_slips, populate_pay_stub, paystub_print



def index(req):

  cursor = utils.get_cursor()
  populate_response = populate_pay_stub.populate_pay_stub(temp = True, incursor = cursor)
  weekly = queries.weekly_pay(incursor=cursor, label=False)
  
  payroll_sql = '''
	SELECT week_of,
	round(sum(hours_worked)) as hours_worked,
	round(avg(hours_worked)) as avg_hours_worked,
  count(person_id) as num_employees,
  round(sum(weekly_pay - nys_withholding - fed_withholding - social_security_tax - medicare_tax)) as payroll
  from   
  %(table_name)s
  where yearweek(week_of) > yearweek(now() - interval '5' week)
  and last_name not in ('Kobrin', 'Labossier', 'Kanarova')
  group by yearweek(week_of)
	order by yearweek(week_of) desc
  '''

  new_payroll = utils.select(
    payroll_sql%{ 'table_name' : 'PAY_STUB_TEMP'},
    incursor=cursor,
    label=False
  )

  past_payroll = utils.select(
    payroll_sql%{ 'table_name' : 'PAY_STUB'},
    incursor=cursor,
    label=False
  )

  detail = utils.select('''
	SELECT concat(yearweek(intime),' ',dayname(intime),' ',date),
	last_name, 
	first_name,
	time_in, 
	time_out, 
	hours_worked 
	from hours_worked 
  where yearweek(intime) > yearweek(now() - interval '5' week)
	order by yearweek(intime) desc, last_name, date(intime)''',
    incursor=None,
    label=False
  )

  html = (
    '''  
      <html>
      <body>
  ''' )
  if populate_response:
    html += '<h1>' + populate_response + '</h1>'
  else:  
    html +='''
	<form action="print_slips.htm" method="POST">
  	<input type="submit" value="commit paystubs">
	</form>
    '''
  html += (
    utils.tohtml(
      'Hours worked per week by person',
       ('week of', 'last name',  'first name', 'hours worked', 'rate', 'gross wage', 'tax', 'net weekly wage', 'tips', 'total pay', 'total hourly', 'tip details'),
      weekly
    ) +
    utils.tohtml(
      'New Payroll',
      ('yearweek', 'hours_worked', 'avg_hrs', '# employees', 'payroll'), 
      new_payroll,
      breakonfirst = True
    ) +
    utils.tohtml(
      'Past Payroll',
      ('yearweek', 'hours_worked', 'avg_hrs', '# employees', 'payroll'), 
      past_payroll,
      breakonfirst = True
    ) +
    utils.tohtml(
      "detail hours",
      ('date', 'last_name', 'first_name', 'time_in', 'time_out', 'hours_worked'), 
      detail
    ) +
    '''</body></html>'''
  )

  return html


if __name__ == '__main__':
  print 'hi'
