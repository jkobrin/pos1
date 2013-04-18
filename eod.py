
import json
import MySQLdb
import utils
import queries


def index(req, lag=0):

  results = queries.nightly_sales_by_server(lag_days=lag)

  #seven_day_total = utils.select('''
  #  SELECT sum(total) night, sum(dtotal) lunch  
  #  FROM nd_tots  
  #  WHERE dat > now() - INTERVAL '7' DAY''',
  #  incursor=None,
  #  label=False
  #)

  #avg = utils.select('''
  #  SELECT sum(total)/2 night, sum(dtotal)/2 lunch  
  #  FROM nd_tots  
  #  WHERE dat > now() - INTERVAL '14' DAY;''',
  #  incursor=None,
  #  label=False
  #)

  #day_totals = utils.select('''select * from nd_tots order by dat desc''', incursor=None, label=False)
  
  grand_total = utils.select('''
    SELECT total, dtotal  
    FROM nd_tots  
    WHERE dat = date(now());''',
    incursor=None,
    label=False
  )
  
  html = (
    '''  
      <html>
      <body>
    ''' + 
#    utils.tohtml(
#      'Nightly Receipts by Server',
#      ('Server', 'ccid', 'Receipts', 'Taxable', 'Tabs Closed'), 
#      results
#    ) +
    utils.tohtml(
      "Nightly Total",
      ('Dinner','Lunch'), 
      grand_total
    ) +

   # utils.tohtml(
   #   "7 day Total",
   #   ('Dinner','Lunch'), 
   #   seven_day_total
   # ) +
   # utils.tohtml(
   #   "2 week average",
   #   ('Dinner','Lunch'), 
   #   avg
   # ) +

#    utils.tohtml(
#      "Day Totals",
#      ('Dinner', 'Day', 'Date','Lunch'), 
#      day_totals
#    ) +
    '''</body></html>'''

  )

  return html

if __name__ == '__main__':
  print index(None)
