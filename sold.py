
import json
import MySQLdb
import utils
import config


def index(req, item_name=None):

   
  results = utils.select('''
  select date(created - interval daynumber day) week, item_name, sum(count), 
  group_concat(concat_ws(' ', dayname(created), count) order by created SEPARATOR ',') detail
  from
  (SELECT 
	item_name, count(*) count, (weekday(created) + 1) MOD 7 as daynumber, created
	from order_item 
  where is_cancelled = false 
  and item_name rlike %s
	group by item_name, date(created)
  ) items_per_day
  group by yearweek(created), item_name
	order by date(created) desc, item_name
  ''',
    incursor=None,
    label=False,
    args=[item_name]
  )
  
  # format detail
  formatted_results = []
  for row in results:
    detail = row[-1] #last field
    detail = dict(d.split(' ') for d in detail.split(','))
    det_string = ' | '.join(
      ('%s %s' % (dayname[:3], detail.get(dayname, 0))
      for dayname in ('Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday')
    ))
    formatted_results.append(row[:-1] + (det_string,))

  html = (
    '''  
      <html>
      <body>
    ''' + 
    utils.tohtml(
      'items sold',
      ('week of', 'name', 'count', 'detail'), 
      formatted_results

    ) +
    '''</body></html>'''
  )

  return html

if __name__ == '__main__':
  index(None, 'steak')
