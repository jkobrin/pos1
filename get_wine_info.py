import json
import MySQLdb
import utils

#log = open('/tmp/logq', 'a')


def index(req, menu_item_id):

  results = utils.select('''
    SELECT frontprice from winelist
    where id = %(menu_item_id)s'''%locals()
  )
  
  if len(results) == 1:
    retval = results[0]
  else:
    retval = None

  return json.dumps(retval)


if __name__ == '__main__':
  print index(None, -1)
  print index(None, 1)
