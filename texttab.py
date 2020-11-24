import json, re, utils
import MySQLdb
from gift_cert import GiftCert
import config_loader
from config import expand_extra_fields
from config import TAXRATE

TEXTWIDTH = 18
NUMWIDTH = 7 

MSG = '''.'''

def index(req, table):
  tab_text, gift_certs = get_tab_text(table)
  return json.dumps(tab_text)

def format_item(name, cnt):
  ret = ' '.join([word for word in name.split() if not word.isdigit()][:3])[:TEXTWIDTH]
  if cnt > 1: 
    ret += ' @'+str(cnt)
  return ret

def is_staff(table_id):
  # this is not currently used for anything
  return re.match('[A-Z][a-z]+ [A-Z][a-z]+', table_id)

def is_gift(item):
  return item['name'].startswith('gift')

def is_printable(item):
  return item['printable']

def is_gratuity(item):
  return item['name'].startswith('gratuity')

def get_tab_text(table, serverpin = None, cursor = None, ogid = None, closed_time = None, admin_view=False, reopen_time = None):

  if cursor is None:
    cursor = utils.get_cursor()
    
  items_query = '''
    SELECT count(*) cnt, og.table_id, oi.id, oi.item_name name, sum(oi.price) price, oi.is_comped, oi.taxable, 
      oi.is_cancelled,
      og.pickup_time,
      og.closedby,
      time_format(timediff(oi.created, og.created), '+%%H:%%i') creat_time,
      time_format(timediff(oi.updated, oi.created), '+%%H:%%i') updat_time,
      oi.created > '%(reopen_time)s' as creat_after,
      oi.updated > '%(reopen_time)s' as updat_after,
      sku.extra
    FROM order_group og 
    JOIN order_item oi ON og.id = oi.order_group_id
    LEFT OUTER JOIN sku ON oi.menu_item_id = sku.id
    WHERE (og.is_open = TRUE and "%(closed_time)s" = 'None' or og.updated = "%(closed_time)s") and og.table_id = "%(table)s"
    and (oi.is_cancelled = FALSE or '%(serverpin)s' = 'NULL' or %(admin_view)s)
    group by oi.item_name, oi.is_comped, oi.is_cancelled, oi.price, IF(item_name rlike 'gift|QR', oi.id, 1)
    '''

  if admin_view: items_query += ', oi.id\n' # don't group for admin_view
  items_query  += '''order by oi.created'''
  items_query = items_query % locals()

  items = utils.select(items_query, cursor)
  if not items: 
    return "no tab opened for table %s" %table, []

  original_serverpin = items[0]['closedby']
  if not serverpin or serverpin == 'NULL':
    serverpin = original_serverpin

  if serverpin:
    servername = utils.select(
      "select coalesce(nickname, first_name) name from person where id = %(serverpin)s"
      % locals(), cursor)[0]['name']
  else:
    servername = 'staff'
 
  foodtotal = sum(item['price'] for item in items if not item['is_cancelled'] and not item['is_comped'])
  taxable_total = sum(item['price'] for item in items if not item['is_cancelled'] and not item['is_comped'] and item['taxable'])
  tax = round(taxable_total*TAXRATE, 2)
  total = foodtotal + tax

  tabtext = ''
  for line in config_loader.config_dict['guest_check_header'].splitlines():
    tabtext += line.center(NUMWIDTH + TEXTWIDTH) + '\n'

  now = utils.now()
  tabtext += '\n  Table:%s  %s  \n\n' % (table,  closed_time or now)
  if items[0]['pickup_time']:
    tabtext += '  Pickup Time:\n %s\n\n' % items[0]['pickup_time'] 

  tabtext += 'FOOD & DRINK' + "\n" 

  divider = '-'*(NUMWIDTH + TEXTWIDTH) + "\n"
  tabtext += divider

  gift_certs = []
  if config_loader.config_dict.get("autoprint_png"):
    gift_certs.append(GiftCert({'name': 'auto', 'filename': config_loader.config_dict['autoprint_png']}))

  gratuity = 0
  gratuity_rate = 0

  for item in items:
    expand_extra_fields(item)
    if is_gratuity(item):
      gratuity_rate = item['price']
      gratuity = round((taxable_total) * gratuity_rate/100.0, 2)
      total = total + gratuity
      continue
    if is_gift(item) or item.get('printable'):
      gift_certs.append(GiftCert(item))
    if item['price'] == 0 and not admin_view:
      continue
    if item['is_cancelled']:
      price = 'cancelled'
    elif item['is_comped']:
      price = 'comped'
    else:  
      price = '%.2f'%item['price']

    tabtext += format_item(item['name'], item['cnt']).ljust(TEXTWIDTH) + price.rjust(NUMWIDTH) + "\n"
    if admin_view:
      tabtext += '<a style="font-size:12; color: green">' 
      if item['creat_after'] : tabtext += '<a style="color: red">'
      tabtext += str(item['creat_time']).replace('+00:', '+').replace('+0', '+') 
      if item['creat_after'] : tabtext += '</a>'
      if item['updat_after'] : tabtext += '<a style="color: red">'
      tabtext += ' ' + str(item['updat_time'] or '').replace('+00:', '+').replace('+0', '+')
      if item['updat_after'] : tabtext += '</a>'
      tabtext += '</a><br/>'

  foodtotal, tax, gratuity, total = (
    ('%.2f'%x).rjust(NUMWIDTH) for x in (foodtotal, tax, gratuity, total)
  )

  tabtext += '\n' + \
    'SUBTOTAL'.ljust(TEXTWIDTH) + foodtotal + '\n'
  tabtext += 'TAX'.ljust(TEXTWIDTH) + tax + '\n'
  if gratuity_rate != 0:
    tabtext += ('GRATIUITY %s%%'%gratuity_rate).ljust(TEXTWIDTH) + gratuity + '\n'
  tabtext += divider
  tabtext += 'TOTAL'.ljust(TEXTWIDTH) + total + '\n'
  tabtext += '''

      Thank You.
    
       - %s



%s
''' % (servername, MSG)

  return tabtext, gift_certs


if __name__ == '__main__':
  tabtext, gift_certs = get_tab_text('Joshua Kobrin', 9175)

  print tabtext
  print gift_certs
