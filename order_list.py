
import re, yaml
import utils
import viewtab

def expand_extra_fields(row):
  
  if row['mynotes']:
    for dct in re.findall('{[^}]*}', row['mynotes']):
      row.update(yaml.load(dct))


def index(req):

  supercat = req.parsed_uri[7]
  if supercat == 'mkt':
    supercat = 'market'

  resp = ''

  results = utils.select('''
    select * from sku_inv where active = true and bin > 0 and supercategory = %s order by supplier''', args=supercat
  )

  if not results:
    return 'no such category as %s'%supercat

  supplier = ''
  for row in results:
    expand_extra_fields(row)
    next_supplier = row.get('supplier') or '<NONE>'
    if supplier.lower().strip() != next_supplier.lower().strip():
      supplier = next_supplier
      resp += supplier + '\n'

    if (row['estimated_units_remaining'] is not None and 
        isinstance(row.get('par'), (int, long, float)) and 
        row.get('par') > row['estimated_units_remaining']):

      row.setdefault('order_amt', str(int(round(row['par'] - row['estimated_units_remaining']))) + ' ' + row.get('order_unit', 'ct.'))
      resp += "\t{name} - {order_amt} \t(${wholesale_price}, {estimated_units_remaining} on hand, par is {par})\n".format(**row)

  return resp
