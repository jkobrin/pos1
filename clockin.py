
import json
import MySQLdb
import utils

from mylog import my_logger
log = my_logger

import json
import MySQLdb


def index(serverpin, in_):
  wantsin = (in_ == 'true')
  wantsout = not wantsin

  sqlin = 'INSERT INTO hours VALUES(null, %(serverpin)s, NOW(), 0)' % locals()
  sqlout = 'UPDATE hours SET outtime = NOW() WHERE person_id = %(serverpin)s AND outtime = 0' % locals()

  conn = MySQLdb.connect (host = "localhost",
                        user = "pos",
                        passwd = "pos",
                        db = "pos")

  cursor = conn.cursor()
  isin = _server_is_in(serverpin)
  isout = not isin

  if wantsin and isin:
    resp = 'already clocked in'
  elif wantsin and isout:
    utils.execute(sqlin, cursor)
    resp = 'Clocked in at ' + utils.now()
  elif wantsout and isin:
    res = utils.execute(sqlout, cursor)
    resp = 'Clocked out at ' + utils.now()
  elif wantsout and isout:
    resp = 'already clocked out'
  else:
    resp = 'programming error'
    

  cursor.close()
  conn.close()

  return json.dumps(resp)

def server_is_in(serverpin):
  return json.dumps(_server_is_in(serverpin))

def _server_is_in(serverpin):
  return bool(utils.select('SELECT * FROM hours WHERE person_id = %(serverpin)s AND outtime=0' % locals()) )

if __name__ == '__main__':
  print index(4008, 'false')
