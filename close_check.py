
import json
import MySQLdb

def label_and_jasonize_query_rows(labels, rows):
  labeled_results = dict(zip(labels, rows))
  jasonized_labeled_results = json.dumps(labeled_results)
  return jasonized_labeled_results


def index(req, table):

  conn = MySQLdb.connect (host = "localhost",
                        user = "pos",
                        passwd = "pos",
                        db = "pos")

  cursor = conn.cursor()


  cursor.execute('''
    SELECT oi.item_name, oi.id, oi.price, sum(oi.price)
    FROM order_group og, order_item oi 
    where og.id = oi.order_group_id
    and og.is_open = TRUE
    and og.table_id = "%(table)s"
    and oi.item_cancelled = FALSE
  ''' % locals())
  rows = cursor.fetchall()
  results = label_and_jasonize_query_rows(('name', 'id', 'price', 'sum'), rows))

  cursor.execute('''
    UPDATE order_group_id
    SET is_open = FALSE
    WHERE is_open = TRUE
    AND table_id = %(table)s
  ''' % locals()

  cursor.close ()
  conn.close ()

  return results
