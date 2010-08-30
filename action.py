import json
import MySQLdb

log = open('/tmp/logq', 'a')


def order(req, table, additem=None, removeitem=None):

  conn = MySQLdb.connect (host = "localhost",
                        user = "pos",
                        passwd = "pos",
                        db = "pos")

  cursor = conn.cursor()

  if additem:
    
    open_order_group = None
    for time in (1,2):
      cursor.execute('''
        SELECT id FROM order_group 
        WHERE is_open = TRUE
        AND table_id = "%s"''' % table
      )
      open_order_group = cursor.fetchone()
      if open_order_group:
        break
      else:
        cursor.execute('''
          INSERT INTO order_group VALUES (null, "%(table)s", TRUE, null)
          '''%locals())

    open_order_group = open_order_group[0];
    cursor.execute('''
      INSERT INTO order_item (order_group_id, item_name, price) VALUES
      (%(open_order_group)d, "%(additem)s", 7.0)
      ''' % locals())

  if removeitem:
    cursor.execute('''
      UPDATE order_item oi
      set oi.item_cancelled =TRUE, oi.updated = NOW()
      where oi.id = %(removeitem)s
    ''' % locals())
    
  cursor.execute('''
    SELECT oi.item_name, oi.id
    FROM order_group og, order_item oi 
    where og.id = oi.order_group_id
    and og.is_open = TRUE
    and og.table_id = "%(table)s"
    and oi.item_cancelled = FALSE
  ''' % locals())
  rows = cursor.fetchall()

  order_items = [{'name': row[0], 'id': row[1]} for row in rows]

  cursor.close ()
  conn.close ()

  return json.dumps(order_items)


if __name__ == '__main__':
  print order(None, 'B12', additem='y')
