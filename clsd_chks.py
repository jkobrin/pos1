import sys


import json
import MySQLdb
import utils

import texttab


def index(req, lag_days=1, output_html = True):

  TAXRATE = texttab.TAXRATE 

  query_txt = '''
  # see checks
    SELECT 
      og.table_id, og.created, og.updated closed_time, og.closedby,
      concat(p.last_name, ', ', substr(p.first_name,1,1), '.') server,
      sum(oi.price) sales, 
      sum(ti.price) taxable_sales,
      sum(oi.price) + COALESCE(round(sum(ti.price) * %(TAXRATE)s, 2),0) receipts
    FROM order_group og 
        left outer join order_item oi on og.id = oi.order_group_id 
        left outer join taxable_item ti on ti.id = oi.id,
        person p 
    WHERE oi.is_cancelled = False
    AND oi.is_comped = False
    AND og.closedby = p.id 
    AND date(og.updated - interval '6' HOUR) = date(now() - INTERVAL '%(lag_days)s' DAY)
  '''%locals()

  if lag_days is not None:
    query_txt += '''and date(og.updated - interval '6' hour) = date(now()) - interval '%(lag_days)s' day
    '''%locals()

  query_txt += '''  group by og.table_id, og.updated order by closed_time;'''

  checks = utils.select(query_txt,
    incursor=None,
    label=True
  )

  body = ''
  for row in checks:
    if output_html: body += '<div style="float:left;"> %(created)s to <br> %(closed_time)s <br> by: %(server)s <h1> %(table_id)s $%(receipts).2f</h1>' % row
    tab_text, certs = texttab.get_tab_text(
      table=row['table_id'], 
      serverpin = row['closedby'], 
      cursor = None, 
      closed_time = row['closed_time'])
    
    if output_html: body += '<h2><pre>' + tab_text + '</pre></h2></div>'
    else:
	body += tab_text + '\n\n'

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


  if output_html:
    output = (
    '''  
      <html>
      <body>
    ''' + 
      body
     +
    '''</body></html>'''
    )
  else:
    output = body

  return output

if __name__ == '__main__':
  print index(None, None, output_html = False)
