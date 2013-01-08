import sys


import json
import MySQLdb
import utils



def index(req):

  weekly = utils.select('''
	SELECT yearweek(intime),
	last_name,
	sum(hours_worked) as hours_worked,
  pay_rate, 
  weekly_tax,
  round(sum(hours_worked)*pay_rate - weekly_tax) as weekly_pay
	from hours_worked 
  where yearweek(intime) > yearweek(now() - interval '5' week)
  group by yearweek(intime), last_name 
	order by yearweek(intime) desc, last_name''',
    incursor=None,
    label=False
  )

  payroll = utils.select('''
	SELECT yearweek(intime),
	sum(hours_worked) as hours_worked,
  round(sum(hours_worked*pay_rate)) + 194 + 480 + 750 as payroll
	from hours_worked 
  where yearweek(intime) > yearweek(now() - interval '5' week)
  and last_name not in ('Kobrin', 'DiLemme', 'Kanarova')
  group by yearweek(intime)
	order by yearweek(intime) desc''',
    incursor=None,
    label=False
  )

  detail = utils.select('''
	SELECT concat(yearweek(intime),' ',dayname(intime),' ',date),
	last_name, 
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
    ''' + 
    utils.tohtml(
      'Hours worked per week by person',
      ('yearweek', 'last name',  'hours_worked', 'rate', 'tax', 'weekly_pay'), 
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
      ('date', 'last_name', 'time_in', 'time_out', 'hours_worked'), 
      detail
    ) +
    '''</body></html>'''
  )

  return html

if __name__ == '__main__':
  print 'hi'
