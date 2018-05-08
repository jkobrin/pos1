import json, re, utils
import MySQLdb
from gift_cert import GiftCert

TAXRATE = .08625
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

def is_coupon(item):
  return item['name'].startswith('coupon')

def is_gratuity(item):
  return item['name'].startswith('gratuity')

def get_tab_text(table, serverpin = None, cursor = None, ogid = None, closed_time = None, admin_view=False, reopen_time = None):

  if cursor is None:
    cursor = utils.get_cursor()
    
  items_query = '''
    SELECT count(*) cnt, og.table_id, oi.id, oi.item_name name, sum(oi.price) price, oi.is_comped, oi.taxable, 
      oi.is_cancelled,
      time_format(timediff(oi.created, og.created), '+%%H:%%i') creat_time,
      time_format(timediff(oi.updated, oi.created), '+%%H:%%i') updat_time,
      oi.created > '%(reopen_time)s' as creat_after,
      oi.updated > '%(reopen_time)s' as updat_after
    FROM order_group og 
    JOIN order_item oi ON og.id = oi.order_group_id
    WHERE (og.is_open = TRUE and "%(closed_time)s" = 'None' or og.updated = "%(closed_time)s") and og.table_id = "%(table)s"
    and (oi.is_cancelled = FALSE or '%(serverpin)s' = 'NULL' or %(admin_view)s)
    group by oi.item_name, oi.is_comped, oi.is_cancelled, oi.price, IF(item_name like 'gift%%', oi.id, 1)
    '''
  if admin_view: items_query += ', oi.id\n' # don't group for admin_view
  items_query  += '''order by oi.created'''
  items_query = items_query % locals()

  items = utils.select(items_query, cursor)

  if serverpin and serverpin != 'NULL':
    servername = utils.select(
      "select coalesce(nickname, first_name) name from person where id = %(serverpin)s"
      % locals(), cursor)[0]['name']
  else:
    servername = 'staff'
 
  if not items: 
    return "no tab opened for table %s" %table, []

  foodtotal = sum(item['price'] for item in items if not item['is_cancelled'] and not item['is_comped'])
  taxable_total = sum(item['price'] for item in items if not item['is_cancelled'] and not item['is_comped'] and item['taxable'])
  tax = round(taxable_total*TAXRATE, 2)
  total = foodtotal + tax

  divider = '-'*(NUMWIDTH + TEXTWIDTH) + "\n"

  if utils.is_salumi():
    tabtext = "SALUMI".center(NUMWIDTH + TEXTWIDTH) + '\n'
    tabtext += "5600 Merrick Rd Massapequa".center(NUMWIDTH + TEXTWIDTH) + '\n'
    tabtext += "516-620-0057".center(NUMWIDTH + TEXTWIDTH) + '\n\n'
  else:
    tabtext = "PLANCHA".center(NUMWIDTH + TEXTWIDTH) + '\n'
    tabtext += "931 Franklin Avenue".center(NUMWIDTH + TEXTWIDTH) + '\n'
    tabtext += "Garden City, NY".center(NUMWIDTH + TEXTWIDTH) + '\n'
    tabtext += "516-246-9459".center(NUMWIDTH + TEXTWIDTH) + '\n\n'
  now = utils.now()
  tabtext += '  Table:%s  %s  \n\n' % (table,  closed_time or now)
  tabtext += 'FOOD & DRINK' + "\n" 
  tabtext += divider

  gift_certs = [GiftCert({'name':'coupon'})]
  gratuity = 0
  gratuity_rate = 0

  for item in items:
    if is_gratuity(item):
      gratuity_rate = item['price']
      gratuity = round((taxable_total) * gratuity_rate/100.0, 2)
      total = total + gratuity
      continue
    if is_gift(item) or is_coupon(item):
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
