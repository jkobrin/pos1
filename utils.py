import MySQLdb

def object_from_dict(the_dict):
  class an_object:
    pass

  an_object.__dict__ = the_dict  
  return an_object
    

def label_query_rows(labels, rows):
  labeled_results = [object_from_dict(dict(zip(labels, row))) for row in rows]
  return labeled_results


def select(query):
  conn = MySQLdb.connect (host = "localhost",
                        user = "pos",
                        passwd = "pos",
                        db = "pos")

  cursor = conn.cursor()

  cursor.execute(query)
  rows = cursor.fetchall()
  colnames = [coldesc[0] for coldesc in cursor.description]
  results = label_query_rows(colnames, rows)

  cursor.close()
  conn.close()

  return results
