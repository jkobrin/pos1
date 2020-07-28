import sys


import json
import MySQLdb
import utils

import texttab
from datetime import date, timedelta


def index(req, lag_days=1):

  TAXRATE = texttab.TAXRATE 

  query_txt = '''
  # see checks
    SELECT ro.created as reopen_time, 
      (select concat(first_name, last_name) from person where person.id = ro.closedby) as orig_closedby,
      og.table_id, og.created, og.updated closed_time, og.closedby, 
      oi.is_cancelled, oi.is_comped,
      concat(p.last_name, ', ', substr(p.first_name,1,1), '.') server,
      sum(oi.price) sales, 
      sum(ti.price) taxable_sales,
      sum(oi.price) + COALESCE(round(sum(ti.price) * %(TAXRATE)s, 2),0) receipts
    FROM order_group og 
        join order_item oi on og.id = oi.order_group_id 
        left outer join taxable_item ti on ti.id = oi.id
        left outer join reopened ro on ro.order_group_id = og.id
        left outer join person p on p.id = og.closedby
    WHERE date(og.updated - interval '6' HOUR) = date(now() - INTERVAL '%(lag_days)s' DAY)
  '''%locals()

  if lag_days is not None:
    query_txt += '''and date(og.updated - interval '6' hour) = date(now()) - interval '%(lag_days)s' day
    '''%locals()

  query_txt += '''  group by og.table_id, og.updated, ro.id order by ro.created, closed_time;'''

  checks = utils.select(query_txt,
    incursor=None,
    label=True
  )

  dayviewed = date.today() - timedelta(days=int(lag_days))
  body = '<h1> %s </h1>' % dayviewed.strftime('%A %B %d')
  for row in checks:
    body += '<div style="float:left;"> %(created)s to <br> %(closed_time)s <br> by: %(server)s <h1> %(table_id)s $%(receipts).2f</h1>' % row
    if row['reopen_time']:
        body += '<h1 style="color: red"> REOPENED: <br> %(reopen_time)s <br>original: %(orig_closedby)s</h1>' %row

    tab_text, certs = texttab.get_tab_text(
      table=row['table_id'], 
      serverpin = row['closedby'], 
      cursor = None, 
      closed_time = row['closed_time'],
      admin_view = True,
      reopen_time = row['reopen_time'])

    hi_tab = tab_text.replace(
        'cancelled', '<a style="color:red"> CANCELLED </a>'
        ).replace('comped', '<a style="color:green"> COMPED </a>')


    
    body += '<h2><pre>' + hi_tab + '</pre></h2></div>'

    #body += utils.tohtml(
    #  "hours",
    #  ('date', 'last_name', 'time_in', 'time_out', 'hours_worked'), 
    #  detail
    #) +
    #dets = utils.select('''
    #select og.id, og.table_id, closedby, sum(price)*1.08625, og.created 
    #from revenue_item ri, order_group og 
    #where ri.order_group_id = og.id 
    #and date(og.created) = date(now()) - interval '1' day 
    #group by og.id;
    #''',
    #  incursor=None,
    #  label=False
    #)


  output = (
    '''  
      <html>
      <body>
    ''' + 
      body
     +
    '''</body></html>'''
  )

  return output

if __name__ == '__main__':
  print index(None, None)
