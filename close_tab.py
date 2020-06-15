import json
import utils
import config_loader
import texttab

from mylog import my_logger

#SPRINT_OPTIONS = {
# 'page-border':'double', 'page-left':'48', 'page-top':'36',
#}

#PRINT_OPTIONS = {
# 'page-border':'single', 
# 'page-left':'12',
#  'media':'Custom.3.125x%(page_length)sin',
# 'lpi': '4',
  #'penwidth': '3000', #no effect
#}

#PRINTER_NAME = 'CITIZEN-CT-S310'

#LINES_PER_INCH = 4
#CHARACTERS_PER_INCH = 10 # CUPS default
#PAGE_WIDTH_IN_INCHES = 3.125
#PAGE_WIDTH_IN_CHARS = PAGE_WIDTH_IN_INCHES * CHARACTERS_PER_INCH - 5

def index(req, table, shouldPrint, serverpin):
  my_logger.info(req.get_remote_host()+': server %s closed tab %s'%(serverpin, table))
  shouldPrint = json.loads(shouldPrint) #convert from string to boolean

  cursor = utils.get_cursor()

  receipt_text, gift_certs = texttab.get_tab_text(table, serverpin, cursor)

  results = utils.select('''
    select paid_before_close 
    from order_group 
    where is_open = True
    AND table_id = %s''', args = [table])

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

  if config_loader.config_dict['printer']['ipaddr'] == 'SERVER_INSTALL':
    #utils.print_slip(receipt_text)
    for cert in gift_certs:
      if shouldPrint or cert.is_gift():
        cert.print_out()
    #return json.dumps(None)
    return json.dumps({'receipt_text': receipt_text, 'gift_certs': []})
  else:
    return json.dumps({'receipt_text': receipt_text, 'gift_certs': [gc.value for gc in gift_certs if gc.is_gift()]})


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
