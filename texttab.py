
import json, utils

TAXRATE = .086

TEXTWIDTH = 20
NUMWIDTH = 7 

def index(req, table):
  return json.dumps(get_tab_text(table))

def get_tab_text(table):
  items = utils.select('''
    SELECT oi.item_name name, oi.id id, oi.price price
    FROM order_group og, order_item oi 
    where og.id = oi.order_group_id
    and og.is_open = TRUE
    and og.table_id = "%(table)s"
    and oi.is_cancelled = FALSE
  ''' % locals())

  if not items: 
    return "no tab opened for table %s" %table

  foodtotal = sum(item['price'] for item in items)
  tax = round(foodtotal * TAXRATE, 2)
  total = foodtotal + tax

  foodtotal, tax, total = (
    str(x).rjust(NUMWIDTH) for x in (foodtotal, tax, total)
  )
  divider = '-'*(NUMWIDTH + TEXTWIDTH) + '\n'

  tabtext = 'FOOD' + '\n' 
  tabtext += divider

  for item in items:
    tabtext += item['name'].ljust(TEXTWIDTH) \
      + str(item['price']).rjust(NUMWIDTH) + '\n'

  tabtext += '\n' + \
    'FOOD'.ljust(TEXTWIDTH) + foodtotal + '\n'
  tabtext += 'TAX'.ljust(TEXTWIDTH) + tax + '\n'
  tabtext += divider
  tabtext += 'TOTAL'.ljust(TEXTWIDTH) + total + '\n'

  return tabtext


if __name__ == '__main__':
  print index(None, 'B12')
