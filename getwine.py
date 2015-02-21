
import json
import MySQLdb
import utils
import datetime
from time import mktime
import decimal

import wineprint


def get(req, filtered='yes'):

  #log = open('/var/www/logs', 'a')
  #log.write("recs called\n")
  conn = MySQLdb.connect (host = "localhost",
                        user = "pos",
                        passwd = "pos",
                        db = "pos")

  cursor = conn.cursor()

  if filtered == 'yes':
    recs = utils.select("select * from winelist_inv where bin != '0'", cursor)
  else:
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


def update_winelist(req, edits, newrows):
  edits = json.loads(edits)
  newrows = json.loads(newrows)

  conn = MySQLdb.connect (#host = "localhost",
                        user = "pos",
                        passwd = "pos",
                        db = "pos")

  cursor = conn.cursor()

  log = open('/var/www/logs', 'a')
  log.write("update_winelist called\n")
  log.write(str(edits) + "\n")
  for rowid, fields_and_vals in edits.items():
    setlist = ','.join('%s = %s'%(f, sql_representation(v)) for f, v in fields_and_vals.items() if f != 'estimated_units_remaining')
    sql = "update winelist set " + setlist + " where id = " + rowid + "\n"
    log.write(sql);
    utils.execute(sql, cursor)
  for fields_and_vals in newrows.values():
    for bad_field in ('uid', 'estimated_units_remaining'):
      if fields_and_vals.has_key(bad_field): fields_and_vals.pop(bad_field)

    fields = fields_and_vals.keys()
    values = fields_and_vals.values()
    field_list = ','.join(fields)
    value_list = ','.join(sql_representation(v) for v in values)
    sql = "insert into winelist ("+field_list+") VALUES ("+value_list+")"
    log.write(sql)
    utils.execute(sql, cursor)

  cursor.close ()
  conn.close ()

  wineprint.gen_fodt_and_pdf()


def sql_representation(val):

  if val is None or val == '':
    return "null"
  elif isinstance(val, basestring):
    # enclose strings in double quotes and escape and double
    # quotes in the string
    return '"%s"' %val.replace('"', '\\"')
  else:
    # booleans and numbers
    return str(val)

if __name__ == '__main__':
  print get(None)
