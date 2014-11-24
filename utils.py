import MySQLdb
import datetime
import os
import socket


def hostname():
  return socket.gethostname()


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

def execute(sql, incursor=None):
  
  logs = open("/var/www/logs", 'a')
  logs.write(sql)

  if not incursor:
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos")

    cursor = conn.cursor()
  else:
    cursor = incursor

  cursor.execute(sql)

  if not incursor:
    cursor.close()
    conn.close()

def select_as_html(query, incursor=None):
  if not incursor:
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos")

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



def select(query, incursor=None, label=True):
  
  if not incursor:
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos")

    cursor = conn.cursor()
  else:
    cursor = incursor

  cursor.execute(query)
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


def tohtml(title, headings, rows, breakonfirst=False):  

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
