import sys


import json
import MySQLdb
import utils



def index(req):

  weekly = utils.select('''
	SELECT week(intime), year(intime), 
	last_name,
	sum(hours_worked) as hours_worked,
  pay_rate, 
  weekly_tax,
  round(sum(hours_worked)*pay_rate - weekly_tax) as weekly_pay
	from hours_worked 
  where (week(now()) + year(now())*52) - (week(intime)+year(intime)*52) < 3
  group by year(intime), week(intime), last_name 
	order by year(intime) desc, week(intime) desc, last_name''',
    incursor=None,
    label=False
  )

  payroll = utils.select('''
	SELECT week(intime), year(intime), 
	sum(hours_worked) as hours_worked,
  round(sum(hours_worked*pay_rate)) + 194 + 480 + 750 as payroll
	from hours_worked 
  where (week(now()) + year(now())*52) - (week(intime)+year(intime)*52) < 3
  and last_name not in ('Kobrin', 'DiLemme', 'Kanarova')
  group by year(intime), week(intime)
	order by year(intime) desc, week(intime) desc''',
    incursor=None,
    label=False
  )

  detail = utils.select('''
	SELECT concat('week ', week(intime),' ',dayname(intime),' ',date),
	last_name, 
	time_in, 
	time_out, 
	hours_worked 
	from hours_worked 
  where (week(now()) + year(now())*52) - (week(intime)+year(intime)*52) < 3
	order by week(intime) desc, last_name, date(intime)''',
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
      ('week', 'year', 'last name',  'hours_worked', 'rate', 'tax', 'weekly_pay'), 
      weekly,
      breakonfirst = True
    ) +
    utils.tohtml(
      'Payroll',
      ('week', 'year', 'hours_worked', 'payroll'), 
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
