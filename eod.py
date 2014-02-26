
import json
import MySQLdb
import utils


def index(req, lag=0):

  grand_total = utils.select('''
    SELECT total, dtotal  
    FROM nd_tots  
    WHERE dat = date(now() - INTERVAL '%(lag)s' day);''' % locals(),
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
