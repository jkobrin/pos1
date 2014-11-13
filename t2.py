import sys


import json
import MySQLdb
import utils



def index(req):

  weekly = utils.select('''
	select
  first_name,
  last_name,
	round(sum(hours_worked),2) as hours_worked,
  round(sum(hours_worked)*pay_rate - weekly_tax) as weekly_pay
	from hours_worked 
  where yearweek(intime) = yearweek(now() - interval '1' week)
  group by yearweek(intime), last_name, first_name
	order by last_name''',
    incursor=None,
    label=False
  )


  output = '_ '*40 + '\n'*3

  for first_name, last_name, hours_worked, weekly_pay in weekly:
    if last_name in ('Kobrin', 'Kanarova'):
      continue

    output += (
      ' '*4 + first_name.ljust(12) + ' '+last_name.ljust(12) + '$'+str(int(weekly_pay or 0)).ljust(6) +
      str(hours_worked).rjust(30) + ' hrs'+'\n'*2  +
       '_ '*40 + '\n'*3
    )   

  return output

if __name__ == '__main__':
  print 'hi'
