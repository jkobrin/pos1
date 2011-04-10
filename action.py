import json
import MySQLdb
import utils

#log = open('/tmp/logq', 'a')


def order(req, table, additem=None, removeitem=None, price=None):

  if table == 'null': return json.dumps(None)

  assert len(table) <= 3, "table ID must be 3 or fewer chars"

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
          INSERT INTO order_group VALUES (null, "%(table)s", TRUE, null, null)
          '''%locals())

    open_order_group = open_order_group[0];
    cursor.execute('''
      INSERT INTO order_item (order_group_id, item_name, price) VALUES
      (%(open_order_group)d, "%(additem)s", "%(price)s")
      ''' % locals())

  if removeitem:
    cursor.execute('''
      UPDATE order_item oi
      set oi.is_cancelled =TRUE, oi.updated = NOW()
      where oi.id = %(removeitem)s
    ''' % locals())
    
  order_item_query = '''   
    SELECT 
      oi.item_name, og.table_id,
      oi.id, oi.is_delivered, oi.is_comped,
      TIMESTAMPDIFF(MINUTE, oi.created, now()) minutes_old
    FROM order_group og, order_item oi 
    where og.id = oi.order_group_id
    and og.is_open = TRUE
    and oi.is_cancelled = FALSE
    '''

  if table != 'ALL': order_item_query += 'and og.table_id = "%s"' % table

  order_items = utils.select(order_item_query, cursor)

  cursor.close ()
  conn.close ()

  return json.dumps(order_items)


if __name__ == '__main__':
  print order(None, 'XRTl', additem='food')
