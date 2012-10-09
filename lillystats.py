import sys


import json
import MySQLdb
import utils



def index(req):

  seven_day_total1 = utils.select('''
  SELECT sum(total) night, sum(dtotal) lunch  
  FROM nd_tots  
  WHERE dat > now() - INTERVAL '7' DAY''',
  incursor=None,
  label=False
  )


  seven_day_total2 = utils.select('''
  SELECT sum(total) night, sum(dtotal) lunch  
  FROM nd_tots  
  WHERE dat > now() - INTERVAL '8' DAY''',
  incursor=None,
  label=False
  )

  in_out1 = utils.select('''
	SELECT last_name, 
	time_in, 
	time_out 
	from hours_worked 
  where date(intime) = date(now())
	order by intime;''',
    incursor=None,
    label=False
  )

  in_out2 = utils.select('''
	SELECT last_name, 
	time_in, 
	time_out 
	from hours_worked 
  where date(intime) = date(now() - INTERVAL '1' DAY)
	order by intime;''',
    incursor=None,
    label=False
  )

  fw_stats = utils.select('''
  SELECT dname, dat,
  comped,
  wine_tot,
  n_tot,
  wine_pct
  from fw_tots_and_staff
  WHERE dat > now() - INTERVAL '7' DAY
  ORDER by dat desc;''',

    incursor=None,
    label=False
  )

  html = (
    '''  
      <html>
      <body>
    ''' + 
    utils.tohtml(
      'Total today',
      ('Night', 'Lunch'), 
      seven_day_total1 
    ) +
    utils.tohtml(
      'Total yesterday',
      ('Night', 'Lunch'), 
      seven_day_total2 
    ) +
    utils.tohtml(
      'Clocked in today',
      ('Name', 'In', 'Out'), 
      in_out1 
    ) +
    utils.tohtml(
      'Clocked in yesterday',
      ('Name', 'In', 'Out'), 
      in_out2 
    ) +
    utils.tohtml(
      'FW Stats',
      ('Day', 'Date', 'Comped', 'Wine', 'Total','Percentage'),
      fw_stats
    ) +
    '''</body></html>'''
  )

  return html




if __name__ == '__main__':
  print 'hi'
