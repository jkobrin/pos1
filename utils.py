import inspect

import MySQLdb
import datetime
import os
import socket
import tempfile, os, subprocess
from mylog import my_logger

def hostname():
  po = passed_options()
  if po and po.has_key('VHOST'):
    return passed_options()['VHOST']
  else:  
    return socket.gethostname()


def passed_options():
  # mod_python for Apache does not put SetEnv directives from apache config into
  # os.environ. This would allow you to know which virtual host, for example, had
  # invoked the code. But they don't pass it in, probably because it can't really
  # be done in a thread-safe way. What they do have is PythonOption which you can
  # set in VirtualHost sections of apache config files and then get from the
  # request object. It is not a global (again, probably cause this cannot be
  # thread-safe) so normally you'd have to pass the request object all down the
  # stack so various functions you call could get the options and know what
  # environment they were operating in. To avoid all the messy parameter
  # passing, we just inspect the stack directly here. The outermost frame is
  # always the same when this code is invoked by the web server: it is the main
  # request handling function the is invoked in mod_python. In this stack frame
  # the local variable "options" contains the PythonOptions set in the apache
  # config. We get it in this utility function and pass it back so it is
  # avaialable to all code in a thread-safe, non-messy way.

  outermost_frame = inspect.stack()[-1][0] 
  # -1 meaning the last thing in list, i.e., the outermost frame, and 0 meaning
  # that the first thing in the tuple representing the frame is the actual frame
  # object itself which is what we need.

  return outermost_frame.f_locals.get('options')
  # will return None if no options, else options is a dict


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
                          db = "pos", 
                          charset = "utf8")

    return conn.cursor()


def execute(sql, incursor=None, args= None):
  
  my_logger.info(sql)

  if not incursor:
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos",
                          charset = "utf8")

    cursor = conn.cursor()
  else:
    cursor = incursor

  cursor.execute(sql, args)

  if not incursor:
    cursor.close()
    conn.close()

def select_as_html(query, incursor=None):
  if not incursor:
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos",
                          charset = "utf8")

    cursor = conn.cursor()
  else:
    cursor = incursor

  cursor.execute(query)
  rows = cursor.fetchall()
  colnames = [coldesc[0] for coldesc in cursor.description]

  if not incursor:
    cursor.close()
    conn.close()

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
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos",
                          charset = "utf8")

    cursor = conn.cursor()
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
    conn.close()

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


if __name__ == '__main__':
  print tohtml('goo', [{3: 'ewew', 5: 'hud'},{3: 'ewjd', 5: 'gf'}, {3: 'ewew', 5: 'hioud'},]) 
