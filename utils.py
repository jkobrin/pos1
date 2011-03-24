import MySQLdb

def object_from_dict(the_dict):
  class an_object:
    pass

  an_object.__dict__ = the_dict  
  return an_object
    

def label_query_rows(labels, rows):
  labeled_results = [dict(zip(labels, row)) for row in rows]
  return labeled_results


def execute(sql, incursor=None):
  
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


def select(query, incursor=None):
  
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
  results = label_query_rows(colnames, rows)

  if not incursor:
    cursor.close()
    conn.close()

  return results
