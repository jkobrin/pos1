import json
import MySQLdb
import utils

#log = open('/tmp/logq', 'a')


def order(req, table, additem=None, removeitem=None, price=None, menu_item_id = None):

  if table == 'null': return json.dumps(None)

  assert len(table) <= 64, "table ID must be 64 or fewer chars"

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
          INSERT INTO order_group VALUES (null, "%(table)s", TRUE, null, null, null)
          '''%locals())

    open_order_group = open_order_group[0];
    cursor.execute('''
      INSERT INTO order_item (order_group_id, item_name, price, menu_item_id) VALUES
      (%(open_order_group)d, "%(additem)s", "%(price)s", "%(menu_item_id)s")
      ''' % locals())

  if removeitem:
    cursor.execute('''
      UPDATE order_item oi
      set oi.is_cancelled =TRUE, oi.updated = NOW()
      where oi.id = %(removeitem)s
    ''' % locals())

    # close tables with no un-cancelled items left
    # TODO: make sure this works...Also: is this really
    # necessary? Could just leave it open.
    cursor.execute('''
      UPDATE order_group og
      set og.is_open = False, updated = now(), closedby = null
      where id = (select order_group_id from order_item oi where oi.id = %(removeitem)s)
      and NOT EXISTS (
        select 1 from order_item oi 
        where order_group_id = og.id
        and oi.is_cancelled = False );
    ''' % locals())


    
  if table == 'ALL': order_item_query = '''SELECT concat(IF(count(*) > 1, concat(count(*),'X '), ''), oi.item_name) as item_name, '''
  else: order_item_query = 'SELECT oi.item_name as item_name, '
  order_item_query += '''   
      og.table_id, 
      oi.id, oi.is_delivered, oi.is_held, oi.is_comped, oi.price,
      TIMESTAMPDIFF(MINUTE, oi.created, now()) minutes_old,
      TIMESTAMPDIFF(MINUTE, oi.updated, now()) minutes_since_mod,
      TIMESTAMPDIFF(SECOND, oi.updated, now()) seconds_since_mod
    FROM order_group og, order_item oi 
    where og.id = oi.order_group_id
    and og.is_open = TRUE
    and oi.is_cancelled = FALSE
    '''
  if table != 'ALL': order_item_query += 'and og.table_id = "%s"\n' % table
  if table == 'ALL': order_item_query += 'group by oi.item_name, og.table_id, oi.is_delivered, oi.is_held, oi.is_comped, oi.price\n'
  order_item_query += 'order by oi.is_held, oi.created, oi.id'

  order_items = utils.select(order_item_query, cursor)

  cursor.close ()
  conn.close ()

  return json.dumps(order_items)


if __name__ == '__main__':
  print order(None, 'XRT', additem='food')
