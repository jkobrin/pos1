import json
import utils
import config_loader
import texttab

from mylog import my_logger

def index(req, table, serverpin):
  my_logger.info(req.get_remote_host()+': server %s closed tab %s'%(serverpin, table))

  results = utils.select('''
    select paid_before_close, (pickup_time > now()) is_before_pickup
    from order_group 
    where is_open = True
    AND table_id = %s''', args = [table])

  if results[0]['is_before_pickup'] == True:
    return json.dumps({'success': False, 'message': "Can't close before pickup time"})
    
  cursor = utils.get_cursor()
  receipt_text, gift_certs = texttab.get_tab_text(table, serverpin, cursor)

  if results[0]['paid_before_close'] == True:
    cursor.execute('''
        UPDATE order_group
        SET is_open = FALSE, updated = now()
        WHERE is_open = TRUE
        AND table_id = %s
      ''', args=[table])
  elif serverpin:    
    cursor.execute('''
        UPDATE order_group
        SET is_open = FALSE, closedby = %s, updated = now()
        WHERE is_open = TRUE
        AND table_id = %s
      ''', args=[serverpin, table])
  else:
    assert ("can't close unpaid tab without server pin")

  cursor.close()

  return json.dumps({
    'success': True,
    'receipt_text': receipt_text, 
    'gift_certs': [gc.get_data_url() for gc in gift_certs]
  })


def set_paid(req, table, val, serverpin):
  my_logger.info(req.get_remote_host()+': server %s tab %s paid: %s'%(serverpin, table, val))

  val = json.loads(val) #convert from string to boolean

  utils.execute('''
      UPDATE order_group
      SET paid_before_close = %s, updated = now(), closedby = %s
      WHERE is_open = TRUE
      AND table_id = %s
    ''', args=[val, serverpin, table])

  return json.dumps(None)
  

def set_pickup(req, table, val):
  my_logger.info(req.get_remote_host()+': tab: %s pickup: %s'%(table, val))

  utils.execute('''
      UPDATE order_group
      SET pickup_time = %s, updated = now()
      WHERE is_open = TRUE
      AND table_id = %s
    ''', args=[val, table])

  return json.dumps(None)
  

if __name__ == '__main__':
  print index(None, 'O1', 'true', 1, close=False)
