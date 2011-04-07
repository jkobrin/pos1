# -*- coding: utf-8 -*-

import MySQLdb

import json, utils

TAXRATE = .08625

TEXTWIDTH = 18
NUMWIDTH = 7 

def index(req, table):
  return json.dumps(get_tab_text(table))

def get_tab_text(table, serverpin = None, cursor = None):

  if cursor is None:
    conn = MySQLdb.connect (host = "localhost",
                          user = "pos",
                          passwd = "pos",
                          db = "pos")

    cursor = conn.cursor()

  items = utils.select('''
    SELECT oi.item_name name, oi.id id, oi.price price
    FROM order_group og, order_item oi 
    where og.id = oi.order_group_id
    and og.is_open = TRUE
    and og.table_id = "%(table)s"
    and oi.is_cancelled = FALSE
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

  foodtotal = sum(item['price'] for item in items)
  tax = round(foodtotal * TAXRATE, 2)
  total = foodtotal + tax

  foodtotal, tax, total = (
    ('%.2f'%x).rjust(NUMWIDTH) for x in (foodtotal, tax, total)
  )
  divider = '-'*(NUMWIDTH + TEXTWIDTH) + "\n"


  tabtext = "SALUMI".center(NUMWIDTH + TEXTWIDTH) + '\n'
  tabtext += "5600 Merrick Rd Massapequa".center(NUMWIDTH + TEXTWIDTH) + '\n'
  tabtext += "516-620-0057".center(NUMWIDTH + TEXTWIDTH) + '\n'
  tabtext += '%s\n' % table
  tabtext += 'FOOD & DRINK' + "\n" 
  tabtext += divider

  for item in items:
    tabtext += item['name'].ljust(TEXTWIDTH) \
      + ('%.2f'%item['price']).rjust(NUMWIDTH) + "\n"

  tabtext += '\n' + \
    'SUBTOTAL'.ljust(TEXTWIDTH) + foodtotal + '\n'
  tabtext += 'TAX'.ljust(TEXTWIDTH) + tax + '\n'
  tabtext += divider
  tabtext += 'TOTAL'.ljust(TEXTWIDTH) + total + '\n'
  tabtext += '''

   Thank You.    (¯`v´¯)
                 `*.¸.*´
    
       - %s
''' % servername

  return tabtext

'''
(¯`v´¯)
`*.¸.*´            
¸.•´¸.•*¨) ¸.•*¨)  
 ¸.• Thank You! *.¸.•´•
(¸.•´               .`
¸¸.•¨¯`•.c u soon.•´

'''

if __name__ == '__main__':
  print get_tab_text('B15')
