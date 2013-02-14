import sys


import json
import MySQLdb
import utils

from texttab import get_tab_text



def index(req, lag_days=1):

  checks = utils.select('''
  # see checks
  select  og.table_id, closedby, sum(price) subtot, sum(price)*1.08625 tot, og.created, og.updated closed_time 
  from order_item oi, order_group og 
  where oi.order_group_id = og.id 
  and oi.is_cancelled = false
  and date(og.created) = date(now()) - interval '%(lag_days)s' day
  group by og.table_id, og.updated order by closed_time;
	'''%locals(),
    incursor=None,
    label=True
  )

  body = ''
  for row in checks:
    body += '<div style="float:left;">time: %(created)s to %(closed_time)s by: %(closedby)s <h1> %(table_id)s $%(tot).2f</h1>' % row
    tab_text, certs = get_tab_text(
      table=row['table_id'], 
      serverpin = row['closedby'], 
      cursor = None, 
      closed_time = row['closed_time'])
    
    body += '<h2><pre>' + tab_text + '</pre></h2></div>'

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



  html = (
    '''  
      <html>
      <body>
    ''' + 
      body
     +
    '''</body></html>'''
  )

  return html

if __name__ == '__main__':
  print 'hi'