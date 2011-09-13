
import json
import MySQLdb
import utils


def get_reopen_id(req, table):

  results = utils.select(
    '''select id, is_open
       from order_group og
       where og.table_id = "%(table)s"
       and og.updated > now() - INTERVAL '20' minute
       order by id desc''' % locals()
  )

  if results and not results[0]['is_open']:
    retval = results[0]['id']
  else:
    retval = None

  return json.dumps(retval)


def index(req, reopen_id):

  utils.execute(
    '''update order_group
       set is_open = True
       where id = "%(reopen_id)s"''' % locals()
  )

  return json.dumps(None)


if __name__ == '__main__':
  print index(None)
