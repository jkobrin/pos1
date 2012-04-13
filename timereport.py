
import json
import MySQLdb
import utils



def index(req):

  weekly = utils.select('''
	SELECT week(intime), 
	last_name, 
	sum(hours_worked) as hours_worked 
	from hours_worked 
  where (week(now()) - week(intime)+52)%52 < 3
  group by year(intime), week(intime), last_name 
	order by year(intime) desc, week(intime) desc, last_name''',
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
  where (week(now()) - week(intime)+52)%52 < 3
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
      'Hours worked per week by server',
      ('week', 'last name', 'hours_worked'), 
      weekly
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
