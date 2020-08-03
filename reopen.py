
import json
import MySQLdb
import utils


def get_reopen_id(req, table):

  results = utils.select(
    '''select id, updated, is_open, closedby
       from order_group og
       where og.table_id = "%(table)s"
       and og.updated > now() - INTERVAL '60' minute
       order by updated desc''' % locals()
  )

  retval = None
  if results:
    last_up = results[0]
    if not last_up['is_open'] and last_up['closedby'] is not None:
      retval = '('+','.join([str(res['id']) for res in results if res['updated'] == last_up['updated']]) + ')'

  return json.dumps(retval)

def record_reopen(req, reopen_id):

  ip = req.get_remote_host()
  
  utils.execute(
    '''insert into reopened 
       select null, '%(ip)s', null, closedby, id
       from order_group
       where id in %(reopen_id)s''' % locals()
  )


def index(req, reopen_id):

  record_reopen(req, reopen_id)

  utils.execute(
    '''update order_group
       set is_open = True, closedby = null, updated = now()
       where id in %(reopen_id)s''' % locals()
  )

  return json.dumps(None)


if __name__ == '__main__':
  print get_reopen_id(None, 'T2')
