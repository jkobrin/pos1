import json
import utils
from mylog import my_logger
import config_loader
import config


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
            delivery_status=0, 
            is_comped=False, 
            parent_item=None,
            incursor=None, **unused):
    
    assert item_id != None, 'item id must not be null' + ' ' + str(locals())
    assert table_id != 'null' and table_id is not None, (
      "table_id cannot be null in call to function 'action/add_item'" + str(locals())
    )  
    assert len(table_id) <= 64, "table_id must be 64 or fewer chars" + str(locals())
    assert item_name is not None, 'item _name required' + str(locals())
    if price is None: price = 0
    #assert price is not None, 'price required' + str(locals())


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
        id, order_group_id, item_name, price, fraction, menu_item_id, taxable, delivery_status, is_comped, parent_item
      ) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''', 
      (item_id, open_order_group, item_name, price, fraction, menu_item_id, taxable, delivery_status, is_comped, parent_item)
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


def synchronize(req, crud_commands, last_update_time):
    my_logger.info((req and req.get_remote_host() or 'no host')+': '+crud_commands +':'+last_update_time)

    crud_commands = json.loads(crud_commands)
    last_update_time = json.loads(last_update_time)

    # first deal with incoming data from this client
    for command in crud_commands:
      if command['command'] == 'add_item':
        add_item(**command)
      if command['command'] == 'cancel_item':
        cancel_item(**command)
      if command['command'] == 'set_status':
        set_status(**command)
  
    # now check if we need a full reload of app
    if last_update_time is not None and config_loader.reload_time() > last_update_time:
      return json.dumps({'instruction': 'reload'}, encoding='latin-1', cls=utils.MyJSONEncoder)

    # now give the client any updates ( which will be those
    # made by other clients (if any) as well as those this client
    # just sent and which were just executed (if any))

    if last_update_time is None:
      update_type = 'replace'
    else:
      update_type = 'incremental'

    if last_update_time is None or config_loader.newconfig_time() > last_update_time:
      newconfig = config.load_config()
    else:
      newconfig = None

    now = utils.select("select now()", label=False)[0][0] #TODO: use fetchOne?
    active_items = get_active_items_updated_since(last_update_time)
    items_by_id = dict((item['id'], item) for item in active_items)

    return json.dumps({
      'instruction': None, 
      'update_type': update_type, 
      'time': now, 
      'config': newconfig,
      'items': items_by_id}, 
      encoding='latin-1', cls=utils.MyJSONEncoder)
    

def get_active_items_updated_since(last_update_time, incursor=None):

  # TODO: Do I really need to join to order_item as oip and get
  # parent's created to determine a pickup time? What is this
  # for? Sorting? Time display? Time display, I think, but this
  # should not be needed for child items anyway. I should axe
  # this. Time display code needs to deal and not even
  # create time display for child items. It isn't used.
  #
  # REMOVED

  select ='''
    SELECT
      og.table_id, 
      og.is_open, 
      og.pickup_time,
      (og.paid_time is not null) as paid_before_close, 
      greatest(oi.updated, oi.created, og.updated, og.created) mod_time,
      oi.created as created_time,
      oi.item_name as item_name, 
      oi.id, 
      oi.price,
      oi.delivery_status,
      oi.is_comped, 
      oi.is_cancelled,
      oi.parent_item,
      oi.menu_item_id,
      oi.fraction,
      oi.taxable,
      sku.supercategory,
      sku.category
    FROM 
      order_group og join 
      order_item oi on og.id = oi.order_group_id left outer join 
      sku on oi.menu_item_id = sku.id
    '''

  full_where = '''
    WHERE 
      og.is_open = TRUE
      and oi.is_cancelled = FALSE
    '''

  incremental_where =  '''
    WHERE
      og.is_open = TRUE
      and (oi.updated >= FROM_UNIXTIME(%s) or oi.created >= FROM_UNIXTIME(%s))
      or og.updated >= FROM_UNIXTIME(%s)
      and (oi.is_cancelled = FALSE or oi.updated >= FROM_UNIXTIME(%s))
    '''

  if last_update_time is None:
    # full update
    return utils.select(select + full_where, incursor)
  else:
    # incremental update
    return utils.select(select + incremental_where, incursor, args=[last_update_time]*4)



if __name__ == '__main__':
  print synchronize(None, '[]', 'null')
