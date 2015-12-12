import json
import MySQLdb
import utils
from mylog import my_logger
import queries

from time import sleep
from random import randint

def get_session_id(req):
    #client will use this to create unique ids for order_item commands it sends to server for DB insertion
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos")
    cursor = conn.cursor()

    cursor.execute("insert into client_session values ()");
    session_id = conn.insert_id()

    cursor.close()
    conn.close()

    return json.dumps(session_id)

  

def add_item(table_id=None, item_name=None, price=None, menu_item_id=None, taxable=True, is_delivered=False, is_comped=False, is_held=False, incursor=None, **unused):
    
    assert table_id != 'null' and table_id is not None, "table_id cannot be null in call to function 'action/add_item'"
    assert len(table_id) <= 64, "table_id must be 64 or fewer chars"
    assert item_name is not None, 'item _name required'
    assert price is not None, 'price required'

    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos")
    cursor = conn.cursor()

    open_order_group = None
    for time in (1,2):
      cursor.execute('''
        SELECT id FROM order_group 
        WHERE is_open = TRUE
        AND table_id = "%s"''' % table_id
      )
      open_order_group = cursor.fetchone()
      if open_order_group:
        break
      else:
        cursor.execute('''
          INSERT INTO order_group VALUES (null, "%(table_id)s", TRUE, null, null, null)
          '''%locals())

    open_order_group = open_order_group[0];
    cursor.execute('''
      INSERT INTO order_item (order_group_id, item_name, price, menu_item_id, taxable, is_delivered, is_comped, is_held) VALUES
      (%(open_order_group)d, "%(item_name)s", "%(price)s", "%(menu_item_id)s", %(taxable)s, %(is_delivered)s, %(is_comped)s, %(is_held)s)
      ''' % locals())

    cursor.close()
    conn.close()


def cancel_item(item_id, incursor=None, **unused):

    utils.execute('''
      UPDATE order_item set is_cancelled =TRUE, updated = NOW() where id = %(item_id)s
    ''' % locals())

    # close tables with no un-cancelled items left
    # TODO: make sure this works...Also: is this really
    # necessary? Could just leave it open.
    utils.execute('''
      UPDATE order_group og
      set og.is_open = False, updated = now(), closedby = null
      where id = (select order_group_id from order_item oi where oi.id = %(item_id)s)
      and NOT EXISTS (
        select 1 from order_item oi 
        where order_group_id = og.id
        and oi.is_cancelled = False );
    ''' % locals())

def set_status(item_id, field, value, **unused):

    utils.execute('''
      UPDATE order_item set %(field)s = %(value)s where id = %(item_id)s
    ''' % locals())



def synchronize(req, crud_commands):
    my_logger.info(req.get_remote_host()+': '+crud_commands)

    crud_commands = json.loads(crud_commands)
    for command in crud_commands:
      if command['command'] == 'add_item':
        add_item(**command)
      if command['command'] == 'cancel_item':
        cancel_item(**command)
      if command['command'] == 'set_status':
        set_status(**command)


    return json.dumps(queries.get_active_items(cook_style=False))
    

def get_active_items(req, cook_style=False, incursor=None):
    #sleep(3)
    return json.dumps(queries.get_active_items(cook_style=cook_style))


def get_cook_items(req):
    return json.dumps(queries.get_active_items(cook_style=True))


if __name__ == '__main__':
  print order(None, 'XRT', additem='food')
