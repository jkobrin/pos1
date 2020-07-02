import json
import MySQLdb
import utils
from mylog import my_logger
import queries

from format_time_diff import format_time_from_now
import datetime
import re 
import yaml


def get_session_id(req):
    #client will use this to create unique ids for order_item commands it sends to server for DB insertion

    my_logger.info(req.get_remote_host()+': get_session_id called')
    cursor = utils.get_cursor()

    cursor.execute("insert into client_session values (null, null);");
    session_id = cursor.lastrowid
    my_logger.info(req.get_remote_host()+': generated session id: %s'%session_id)

    cursor.close()

    return json.dumps(session_id)


def add_item(item_id=None, 
            table_id=None, 
            item_name=None, 
            price=None, 
            fraction=None, 
            menu_item_id=None, 
            taxable=True, 
            is_delivered=False, 
            is_comped=False, 
            is_held=False,
            parent_item=None,
            incursor=None, **unused):
    
    assert item_id != None, 'item id must not be null' + ' ' + str(locals())
    assert table_id != 'null' and table_id is not None, (
      "table_id cannot be null in call to function 'action/add_item'" + str(locals())
    )  
    assert len(table_id) <= 64, "table_id must be 64 or fewer chars" + str(locals())
    assert item_name is not None, 'item _name required' + str(locals())
    if price is None: price = 0
    #Oassert price is not None, 'price required' + str(locals())


    cursor = utils.get_cursor()

    open_order_group = None
    for time in (1,2):
      cursor.execute('''
        SELECT id FROM order_group 
        WHERE is_open = TRUE
        AND table_id = %s''', (table_id,)
      )
      open_order_group = cursor.fetchone()
      if open_order_group:
        break
      else:
        cursor.execute('''INSERT INTO order_group VALUES (null, %s, TRUE, null, null, null, null, null)''', (table_id,))
    open_order_group = open_order_group[0];

    cursor.execute('''
      INSERT INTO order_item (
        id, order_group_id, item_name, price, fraction, menu_item_id, taxable, is_delivered, is_comped, is_held, parent_item
      ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
      (item_id, open_order_group, item_name, price, fraction, menu_item_id, taxable, is_delivered, is_comped, is_held, parent_item)
    )

    cursor.close()


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
      where id = (select order_group_id from order_item oi where oi.id = %s)
      and NOT EXISTS (
        select 1 from order_item oi 
        where order_group_id = og.id
        and oi.is_cancelled = False );
    '''% item_id)

def set_status(item_id, field, value, **unused):

    utils.execute('''
      UPDATE order_item set %(field)s = %(value)s, updated = now() where id = %(item_id)s
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
  
    active_items = queries.get_active_items()
    for item in active_items:

      item['time_display'] = (item['is_pickup'] and 'P' or '') + format_time_from_now(datetime.datetime.now(), item['pickup_time'])
      if item['minutes_since_mod'] is not None and not item['is_pickup']:
        item['time_display'] += ' ~%s'%item['minutes_since_mod']
      if datetime.datetime.now().date() == item['pickup_time'].date():
        item['time_category'] = "Today";
      elif datetime.datetime.now().date() < item['pickup_time'].date():  
        item['time_category'] = "Future";
      else:  
        item['time_category'] = "Past";

    return json.dumps(active_items, encoding='latin-1', cls=utils.MyJSONEncoder)
    


if __name__ == '__main__':
  print order(None, 'XRT', additem='food')
