import json
import MySQLdb
import utils

from mylog import my_logger
log = my_logger

def index(req, p_from, p_to):
  # What does the 'p' stand for in these argument names? parameter?
  # I have no recollection.
  log.debug('move tab : ' + p_from + "  " + p_to)

  cursor = utils.get_cursor()

  paid_pickup = utils.select('''
    select sum(paid_time) paid, sum(pickup_time) pickup_time
    from order_group 
    where is_open=true
    and table_id in (%s, %s)''',
    args=[p_to, p_from], incursor=cursor)[0]
  

  if not paid_pickup['pickup_time'] and not paid_pickup['paid']:
    utils.execute(
      '''update order_group
        set table_id = %s, updated = now()
        where table_id = %s
        and is_open = true
        ''', 
       args=[p_to, p_from], 
       incursor = cursor
    )

    retval = {'success': True, 'message': None}
  else:  
    retval = {'success': False, 'message': 'can not move or combine tabs marked paid or with pickup time'}

  cursor.close()
  return json.dumps(retval)


if __name__ == '__main__':
  cursor = utils.get_cursor()
  paid_pickup = utils.select('''
    select sum(paid_time) paid, sum(pickup_time) pickup_time
    from order_group 
    where is_open=true
    and table_id in (%s, %s)''',
    args=['O4', 'O3'], incursor=cursor)[0]
  

  cursor.close()
  print paid_pickup

