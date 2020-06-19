import json
import utils
import datetime
from time import mktime
import decimal

import wineprint


def get_catering(req):
  return get_inventory("select * from sku_inv where supercategory = 'catering' and bin != '0' order by id")

def get_mkt(req):
  return get_inventory("select * from sku_inv where supercategory = 'market' and bin != '0' order by id")

def get_cafe(req):
  return get_inventory("select * from sku_inv where supercategory = 'cafe' and bin != '0' order by id")

def get_food(req):
  return get_inventory("select * from sku_inv where supercategory = 'food' and bin != '0'")

def get_bev(req):
  return get_inventory("select * from sku_inv where supercategory = 'bev' and bin is not null order by category, bin")

def get_allbev(req):
  return get_inventory("select * from sku_inv where supercategory = 'bev'")

def get_wine(req):
  return get_inventory('''
    select * from sku_inv where supercategory = 'bev' 
    and bin is not null and bin != 0 and category rlike '^red|^white &|^bubbly'
    order by category, bin''')

def get_beer(req):
  return get_inventory('''
    select * from sku_inv where supercategory = 'bev' 
    and bin is not null and bin != 0 and category rlike 'Beer'
    order by bin''')

def get_cocktails(req):
  return get_inventory('''
    select * from sku_inv where supercategory = 'bev' 
    and bin is not null and bin != 0 and category rlike 'Cocktails'
    order by bin''')

def get_winebeer(req):
  return get_inventory('''
    select * from sku_inv where supercategory = 'bev' 
    and bin is not null and bin != 0 and category rlike 'Wine|Before & After|Dessert|Bubbly|Beer'
    order by bin''')


def get_by_upc(upc):
  recs = utils.select("select * from sku_inv where upc = %s", args=upc)
  return json.dumps(recs, cls=utils.MyJSONEncoder)

def get_by_id(id):
  recs = utils.select("select * from sku_inv where id= %s", args=id)
  return json.dumps(recs, cls=utils.MyJSONEncoder)

def get_by_name(name):
  recs = utils.select("select * from sku_inv where name = %s", args=name)
  return json.dumps(recs, cls=utils.MyJSONEncoder)

def get_inventory(select):
  recs = utils.select(select)
  return json.dumps(recs, cls=utils.MyJSONEncoder)

def field_names():
  fields = utils.select('desc sku_inv')
  field_names = [field['Field'] for field in fields]
  return json.dumps(field_names)

def sku_names():
  sku_names = utils.select('select concat(supercategory, ":", category, ":", name) as name, id from sku where bin is not null and bin > 0')
  return json.dumps(sku_names)

def update(req, edits, newrows):
  edits = json.loads(edits)
  newrows = json.loads(newrows)
  insert_ids = {}
  cursor = utils.get_cursor()

  for rowid, fields_and_vals in edits.items():
    setlist = ','.join('%s = %s'%(f, sql_representation(v)) for f, v in fields_and_vals.items() if f != 'estimated_units_remaining')
    sql = "update sku set " + setlist + " where id = " + rowid + "\n"
    utils.execute(sql, cursor)
  for rowid, fields_and_vals in newrows.items():
    for bad_field in ('uid', 'undefined', 'estimated_units_remaining', 'boundindex', 'visibleindex', 'uniqueid'):
      if fields_and_vals.has_key(bad_field): fields_and_vals.pop(bad_field)

    fields = fields_and_vals.keys()
    values = fields_and_vals.values()
    field_list = ','.join(fields)
    value_list = ','.join(sql_representation(v) for v in values)
    sql = "insert into sku ("+field_list+") VALUES ("+value_list+")"
    utils.execute(sql, cursor)
    insert_ids[rowid] = utils.select("select LAST_INSERT_ID()", cursor, False)[0][0]

  cursor.close ()

  wineprint.gen_fodt_and_pdf()

  return json.dumps(insert_ids)


def sql_representation(val):

  if val is None or val == '':
    return "null"
  elif isinstance(val, basestring):
    # enclose strings in double quotes and escape and double
    # quotes in the string
    return '"%s"' %val.replace('"', '\\"')
  else:
    # booleans and numbers
    return str(val)

if __name__ == '__main__':
  print get(None)
