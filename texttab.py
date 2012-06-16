import json, utils
import MySQLdb


TAXRATE = .08625
TEXTWIDTH = 18
NUMWIDTH = 7 
add_grat = False

def index(req, table):
  return json.dumps(get_tab_text(table))

def format_item(name, cnt):
  ret = ' '.join([word for word in name.split() if not word.isdigit()][:3])[:TEXTWIDTH]
  if cnt > 1: 
    ret += ' @'+str(cnt)
  return ret

def get_tab_text(table, serverpin = None, cursor = None, ogid = None, closed_time = None):

  if cursor is None:
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos")

    cursor = conn.cursor()

  items = utils.select('''
    SELECT count(*) cnt, oi.item_name name, sum(oi.price) price, oi.is_comped
    FROM order_group og, order_item oi 
    where og.id = oi.order_group_id
    and (og.is_open = TRUE and og.table_id = "%(table)s" and "%(ogid)s" = "None" or og.id = "%(ogid)s")
    and oi.is_cancelled = FALSE
    group by oi.item_name, oi.is_comped
    order by oi.id
  ''' % locals(),
    cursor)

  if serverpin:
    servername = \
      utils.select(
        "select first_name from person where id = %(serverpin)s" % locals(),
        cursor
        )[0]['first_name']
  else:
    servername = 'Salumi'
 
  if not items: 
    return "no tab opened for table %s" %table

  foodtotal = sum(item['price'] for item in items if not item['is_comped'])
  notaxtotal = sum(item['price'] for item in items if item['name'].startswith('gift'))
  tax = round((foodtotal - notaxtotal) * TAXRATE, 2)
  gratuity = round(foodtotal * .18, 2)
  total = foodtotal + tax 
  if add_grat:
    total = total + gratuity

  foodtotal, tax, gratuity, total = (
    ('%.2f'%x).rjust(NUMWIDTH) for x in (foodtotal, tax, gratuity, total)
  )
  divider = '-'*(NUMWIDTH + TEXTWIDTH) + "\n"

  tabtext = "SALUMI".center(NUMWIDTH + TEXTWIDTH) + '\n'
  tabtext += "5600 Merrick Rd Massapequa".center(NUMWIDTH + TEXTWIDTH) + '\n'
  tabtext += "516-620-0057".center(NUMWIDTH + TEXTWIDTH) + '\n\n'
  now = utils.now()
  tabtext += '  Table:%s  %s  \n\n' % (table,  closed_time or now)
  tabtext += 'FOOD & DRINK' + "\n" 
  tabtext += divider

  for item in items:
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
''' % servername

  return tabtext


if __name__ == '__main__':
  print get_tab_text('1')
