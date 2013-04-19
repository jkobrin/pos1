
import json
import MySQLdb
import utils
import datetime
from time import mktime
import decimal

def get(req): #, table, additem=None, removeitem=None, price=None):

  #log = open('/var/www/logs', 'a')
  #log.write("recs called\n")
  conn = MySQLdb.connect (host = "localhost",
                        user = "pos",
                        passwd = "pos",
                        db = "pos")

  cursor = conn.cursor()

  recs = utils.select('''select * from winelist_inv''', cursor)

  cursor.close ()
  conn.close ()

  class MyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, datetime.date):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
          #Decimal type has no json encoding
            return str(obj)

        return json.JSONEncoder.default(self, obj)

  return json.dumps(recs, cls=MyEncoder)


def update_winelist(req, edits): #, table, additem=None, removeitem=None, price=None):
  edits = json.loads(edits)

  conn = MySQLdb.connect (#host = "localhost",
                        user = "pos",
                        passwd = "pos",
                        db = "pos")

  cursor = conn.cursor()

  log = open('/var/www/logs', 'a')
  log.write("update_winelist called\n")
  log.write(str(edits) + "\n")
  for rowid, fields_and_vals in edits.items():
    setlist = ','.join('%s = %s'%(f, sql_representation(v)) for f, v in fields_and_vals.items())
    sql = "update winelist set " + setlist + " where id = " + rowid + "\n"
    log.write(sql);
    utils.execute(sql, cursor)
  cursor.close ()
  conn.close ()

def sql_representation(val):

  if val is None or val == '':
    return "null"
  else:
    # enclose everything else in double quotes; numbers don't
    # need it but it doesn't hurt. Strings and dates do need it.
    return '"%s"' %val

if __name__ == '__main__':
  print bevinventory_records(None)
