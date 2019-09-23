import json
from decimal import Decimal
import MySQLdb
import datetime
import os
import tempfile, os, subprocess
import config_loader
from mylog import my_logger

def object_from_dict(the_dict):
  class an_object:
    pass

  an_object.__dict__ = the_dict  
  return an_object


def label_query_rows(labels, rows):
  labeled_results = [dict(zip(labels, row)) for row in rows]
  return labeled_results

def now():
  return datetime.datetime.now().strftime("%H:%M %m/%d")

def file_slip(text, outfile=None, lang=None):
    slipfile = open(outfile, 'w')
    slipfile.write(text)
    slipfile.close()

def print_slip(text, outfile=None, lang=None):
    slipfile = tempfile.NamedTemporaryFile(delete=False)
    slipfile.write(text.encode('latin1', 'replace'))
    filename = slipfile.name
    slipfile.close()

    args = ['enscript', '--font=Courier-Bold@11/16', '-B', '-MEnv10']
    if outfile is not None: args.append('-o' + outfile)
    if lang is not None: args.append('-w' + lang)
    args.append(filename)

    subprocess.call(args)

    os.remove(filename)


def get_cursor():
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = config_loader.config_dict['db']['name'],
                          charset = "utf8")

    return conn.cursor()


def execute(sql, incursor=None, args= None):
  
  my_logger.info(sql + repr(args))

  if not incursor:
    cursor = get_cursor()
  else:
    cursor = incursor

  cursor.execute(sql, args)

  if not incursor:
    cursor.close()

def select_as_html(query, incursor=None):
  if not incursor:
    cursor = get_cursor()
  else:
    cursor = incursor

  cursor.execute(query)
  rows = cursor.fetchall()
  colnames = [coldesc[0] for coldesc in cursor.description]

  if not incursor:
    cursor.close()

  return rows

def sql_update(table_name, dct, where, where_params, incursor=None):

  sqltext = 'UPDATE %s SET %s where %s'%(table_name, ','.join(col +'=%s' for col in dct.keys()), where)
  execute(sqltext, incursor=incursor, args=dct.values() + where_params)
    

def sql_insert(table_name, dct, incursor=None):

  columns = ', '.join(dct.keys())
  sqltext = 'INSERT into %s (%s) VALUES '%(table_name, columns) + '(' + ','.join(['%s']*len(dct.values())) + ')'
  execute(sqltext, incursor=incursor, args=dct.values())
    

def select(query, incursor=None, label=True, args=None):
  
  my_logger.debug(query)

  if not incursor:
    cursor = get_cursor()
  else:
    cursor = incursor

  cursor.execute(query, args)
  rows = cursor.fetchall()
  colnames = [coldesc[0] for coldesc in cursor.description]

  if label == 'separate':
    return colnames, rows

  if label:
    results = label_query_rows(colnames, rows)
  else:
    results = rows

  if not incursor:
    cursor.close()

  return results



def convert_list_of_dict_2_list_of_list(base_list):

  for item in base_list:
    if type(item) is dict:
      item = item.values()
    yield item


def tohtml(title, headings, rows, breakonfirst=False):  

  rows = convert_list_of_dict_2_list_of_list(rows)

  if breakonfirst:
    ret = "<h1> %(title)s </h1>"%locals()

    subtab = []
    for row in rows:
      if subtab and row[0] != subtab[0][0]:
        #raise Exception('here' + str(row[0]) + str(subtab))
        ret += tohtml(subtab[0][0], headings, subtab, breakonfirst = False)
        subtab = []
      subtab.append(row)
       
    ret += tohtml(subtab[0][0], headings, subtab, breakonfirst = False)
  
    return ret
  else:

    return (
    ''' 
      <h1> %(title)s </h1>
      <table border=1 cellspacing=1 cellpadding=5>
    ''' % locals() +
    "<tr>" + "".join(["<th>%s</th>"%heading for heading in headings]) + "</tr>\n"
    + ''.join(["<tr>"+"".join(["<td>%s</td>"%item for item in row]) + "</tr>\n"
      for row in rows
      ]) +
    '''</table> '''
    )
  
def is_salumi():
  return not is_plancha()

def is_plancha():
  return os.uname()[1] == 'plansrv'

class MyJSONEncoder(json.JSONEncoder):

  def default(self, obj):
      if isinstance(obj, datetime.date):
          return obj.isoformat()
      if isinstance(obj, Decimal):
        #Decimal type has no json encoding
          return str(obj)

      return json.JSONEncoder.default(self, obj)




if __name__ == '__main__':
  print tohtml('goo', [{3: 'ewew', 5: 'hud'},{3: 'ewjd', 5: 'gf'}, {3: 'ewew', 5: 'hioud'},]) 
