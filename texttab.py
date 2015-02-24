import json, re, utils
import MySQLdb
from gift_cert import GiftCert

TAXRATE = .08625
TEXTWIDTH = 18
NUMWIDTH = 7 
GRATUITY18 = 'gratuity18'
GRATUITYRATE = .18

def index(req, table):
  tab_text, gift_certs = get_tab_text(table)
  return json.dumps(tab_text)

def format_item(name, cnt):
  ret = ' '.join([word for word in name.split() if not word.isdigit()][:3])[:TEXTWIDTH]
  if cnt > 1: 
    ret += ' @'+str(cnt)
  return ret

def is_staff(table_id):
  return re.match('[A-Z][a-z]+ [A-Z][a-z]+', table_id)

def is_gift(item):
  return item['name'].startswith('gift')

def get_tab_text(table, serverpin = None, cursor = None, ogid = None, closed_time = None):

  if cursor is None:
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos")

    cursor = conn.cursor()
    
  items_query = '''
    SELECT count(*) cnt, og.table_id, oi.id, oi.item_name name, sum(oi.price) price, oi.is_comped
    FROM order_group og, order_item oi 
    where og.id = oi.order_group_id
    and (og.is_open = TRUE or og.updated = "%(closed_time)s") and og.table_id = "%(table)s"
    and oi.is_cancelled = FALSE
    group by oi.item_name, oi.is_comped, oi.price, IF(item_name like 'gift%%', oi.id, 1)
    order by oi.id
  ''' % locals()


  items = utils.select(items_query, cursor)

  if serverpin:
    servername = utils.select(
      "select coalesce(nickname, first_name) name from person where id = %(serverpin)s"
      % locals(), cursor)[0]['name']
  else:
    servername = 'staff'
 
  if not items: 
    return "no tab opened for table %s" %table, []

  add_grat = GRATUITY18 in (item['name'] for item in items)
  #items =  (item for item in items if item['name'] != GRATUITY18)
  foodtotal = sum(item['price'] for item in items if not item['is_comped'])
  notaxtotal = sum(item['price'] for item in items if item['is_comped'] ==0 and (is_gift(item) or is_staff(items[0]['table_id'])))
  tax = round((foodtotal - notaxtotal) * TAXRATE, 2)
  gratuity = round((foodtotal - notaxtotal) * GRATUITYRATE, 2)
  total = foodtotal + tax
  if add_grat:
    total = total + gratuity

  foodtotal, tax, gratuity, total = (
    ('%.2f'%x).rjust(NUMWIDTH) for x in (foodtotal, tax, gratuity, total)
  )
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

  gift_certs = []

  for item in items:
    if is_gift(item):
      gift_certs.append(GiftCert(item['id'], item['price']))
    if item['price'] == 0:
      continue
    if item['is_comped']:
      price = 'comped'
    else:  
      price = '%.2f'%item['price']

    tabtext += format_item(item['name'], item['cnt']).ljust(TEXTWIDTH) + price.rjust(NUMWIDTH) + "\n"

  tabtext += '\n' + \
    'SUBTOTAL'.ljust(TEXTWIDTH) + foodtotal + '\n'
  tabtext += 'TAX'.ljust(TEXTWIDTH) + tax + '\n'
  if add_grat:
    tabtext += 'GRATIUITY 18%'.ljust(TEXTWIDTH) + gratuity + '\n'
  tabtext += divider
  tabtext += 'TOTAL'.ljust(TEXTWIDTH) + total + '\n'
  tabtext += '''

      Thank You.
    
       - %s



.
''' % servername

  return tabtext, gift_certs


if __name__ == '__main__':
  tabtext, gift_certs = get_tab_text('1', 9175)

  print tabtext
  print gift_certs
