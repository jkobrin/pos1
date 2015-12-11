import json
import MySQLdb
import utils
from mylog import my_logger
import queries

from time import sleep
from random import randint


def order(req, 
  table, 
  additem=None, 
  removeitem=None, 
  price=None, 
  menu_item_id = None, 
  taxable=True, 
  delivered=False): 

  #sleep(randint(0,10))
    

  if removeitem or additem:
    my_logger.info(req.get_remote_host() + 
      ': action/order on table:%(table)s add_item: %(additem)s removeitem: %(removeitem)s  price: %(price)s delivered: %(delivered)s taxable: %(taxable)s'
      %locals()
    )

  assert table != 'null', "table ID cannot be null in call to function 'action/order'"
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
      INSERT INTO order_item (order_group_id, item_name, price, menu_item_id, taxable, is_delivered) VALUES
      (%(open_order_group)d, "%(additem)s", "%(price)s", "%(menu_item_id)s", %(taxable)s, %(delivered)s)
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


  retval = queries.get_active_items(incursor=cursor)
  cursor.close()
  conn.close()
  return json.dumps(retval)


def get_active_items(req, cook_style=False, incursor=None):
    #sleep(3)
    return json.dumps(queries.get_active_items(cook_style=cook_style))


def get_cook_items(req):
    return json.dumps(queries.get_active_items(cook_style=True))


if __name__ == '__main__':
  print order(None, 'XRT', additem='food')
