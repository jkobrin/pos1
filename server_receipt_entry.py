from mylog import my_logger
log = my_logger

import json
import utils


def index(req, serverpin, cctotal=None, cctips=None, cash_drop=None, starting_cash=None, cash_left_in_bank=None):
  data =    {
      'person_id': serverpin,
      'cctotal':cctotal,
      'cctips':cctips,
      'cash_drop': cash_drop,
      'starting_cash': starting_cash,
      'cash_left_in_bank': cash_left_in_bank
  }

  results = utils.select(
    '''select id from server_receipts 
      where date(created - INTERVAL '6' hour) = date(now() - INTERVAL '6' hour)
      and person_id = %s''', args = [serverpin]
  )

  if results:
    row_id = results[0]['id']
    utils.sql_update(table_name = 'server_receipts', dct=data, where='id = %s', where_params = [row_id])
  else:
    dat_results = utils.select('''select date(now() - INTERVAL '6' hour) dat''')
    data['dat'] = dat_results[0]['dat']
    utils.sql_insert('server_receipts', data)

  return json.dumps(str(data))


def get(req, serverpin): 
  results = utils.select(
    '''select cctotal, cctips, cash_drop, starting_cash, cash_left_in_bank 
      from (select 1)x left outer join /* give back one row of nulls when no results */
      server_receipts on person_id = %s
      and date(created - INTERVAL '6' hour) = date(now() - INTERVAL '6' hour)
      ''', args = [serverpin]
  )

  return json.dumps(results[0])


def admin_update(req, receipts_id, field_name, new_value):
  
  utils.execute(
  '''update server_receipts set %(field_name)s = '%(new_value)s' where id = %(receipts_id)s;'''%locals()
  )

  return json.dumps(None)


def admin_new_record(req, serverpin, dat):
    
    utils.execute(
    '''insert into server_receipts (person_id, dat) values (%s, %s)''', args = (serverpin, dat)
    )
  
    results = utils.select(
    '''select id from server_receipts where person_id = %s and dat = %s''', args = [serverpin, dat]
    )
    
    return json.dumps(results[0]['id'])
   

