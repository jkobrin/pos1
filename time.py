import sys


import json
import MySQLdb
import utils, queries, print_pay_slips, populate_pay_stub



def index(req, doprint=0):

  if doprint:
    print_pay()
    print_message="<p> PRINTED.<br>"
  else:
    print_message = ""

  cursor = utils.get_cursor()
  populate_response = populate_pay_stub.populate_pay_stub(temp = True, incursor = cursor)
  weekly = queries.weekly_pay(incursor=cursor)
  

  payroll = utils.select('''
	SELECT yearweek(intime),
	sum(hours_worked) as hours_worked,
  round(sum(hours_worked*pay_rate)) as payroll
	from hours_worked 
  where yearweek(intime) > yearweek(now() - interval '5' week)
  and last_name not in ('Kobrin', 'Labossier', 'Kanarova', 'Rodrigues')
  group by yearweek(intime)
	order by yearweek(intime) desc''',
    incursor=None,
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
	<form action="t1.py?doprint=1" method="POST">
  	<input type="submit" value="print pay slips">
	</form>
    ''' + print_message
  html += (
    utils.tohtml(
      'Hours worked per week by person',
      ('week of', 'last name',  'first_name', 'hours_worked', 'rate', 'tax', 'net weekly wage', 'tips', 'total hourly'),
      weekly,
      breakonfirst = True
    ) +
    utils.tohtml(
      'Payroll',
      ('yearweek', 'hours_worked', 'payroll'), 
      payroll,
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

def print_pay():
    populate_response = populate_pay_stub.populate_pay_stub(temp = False)
    print_pay_slips.go()


if __name__ == '__main__':
  print 'hi'
