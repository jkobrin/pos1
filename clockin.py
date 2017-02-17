import json
import MySQLdb
import utils

from mylog import my_logger
log = my_logger

import json
import utils


def index(serverpin, in_):
  wantsin = (in_ == 'true')
  wantsout = not wantsin

  cursor = utils.get_cursor()

  isin = _server_is_in(serverpin)
  isout = not isin

  if wantsin and isin:
    resp = 'already clocked in'
  elif wantsin and isout:
    tip_share = server_tip_share(serverpin)
    utils.sql_insert('hours', {'person_id': serverpin, 'tip_share': tip_share}, cursor)
    #sqlin = 'INSERT INTO hours VALUES(null, %(serverpin)s, NOW(), 0, %(tip_share)s, null)' % locals()
    resp = 'Clocked in at ' + utils.now()
  elif wantsout and isin:
    sqlout = 'UPDATE hours SET outtime = NOW() WHERE person_id = %(serverpin)s AND outtime = 0' % locals()
    res = utils.execute(sqlout, cursor)
    resp = 'Clocked out at ' + utils.now()
  elif wantsout and isout:
    resp = 'already clocked out'
  else:
    resp = 'programming error'
    

  cursor.close()

  return json.dumps(resp)

def server_is_in(serverpin):
  return json.dumps(_server_is_in(serverpin))

def _server_is_in(serverpin):
  return bool(utils.select('SELECT * FROM hours WHERE person_id = %s AND outtime=0', args=[serverpin]) )

def server_tip_share(serverpin):
  ret = utils.select('SELECT tip_share FROM hours WHERE person_id = %(serverpin)s and tip_share is not null order by id desc LIMIT 1' % locals())
  if ret:
    ts = ret[0]['tip_share'];
  else: 
   ts = 'null'

  return ts


if __name__ == '__main__':
  print index(4008, 'false')
