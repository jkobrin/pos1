import utils
import tempfile, os
import queries
import subprocess
from texttab import TAXRATE
TEXTWIDTH = 25

def go():
    weekly_pay = queries.weekly_pay(printmode = 1)

    for rec in weekly_pay:
      open_tab = total_staff_tab(rec['first_name'], rec['last_name'])
      rec['open_tab'] = open_tab
      rec['payout'] = rec['net_wage']
      if open_tab is not None:
        if open_tab <= rec['net_wage']:
          close_staff_tab(rec['first_name'], rec['last_name'])
          rec['open_tab'] = str(open_tab) + ' CLOSED'
          rec['payout'] = round(float(rec['net_wage']) - float(open_tab))
        else:
          rec['open_tab'] = str(open_tab) + ' STILL OPEN'
          
          
        
      slip_text = get_slip_text(rec)
      slipfile = tempfile.NamedTemporaryFile(delete=False)
      slipfile.write(slip_text)
      filename = slipfile.name
      slipfile.close()
      #testfile = '-p/var/www/slips/%s.ps'%rec['last_name']
      #subprocess.call(['enscript', testfile, '--font=Courier-Bold@11/16', '-B', '-MEnv10', filename])
      subprocess.call(['enscript', '--font=Courier-Bold@11/16', '-B', '-MEnv10', filename])
      print slip_text
      os.remove(filename)
    

def get_slip_text(rec):
    
    text = '''
    {first_name} {last_name} {week_of}
    tips: {tips}
    total hourly: {total_hourly_pay}
    {hours_worked} hours
    {pay_rate} per hr.
    tax: {weekly_tax}
    net wage: {net_wage}
    open tab: {open_tab}

    PAYOUT: {payout}
    '''.format(**rec)

    return text
    

def total_staff_tab(first_name, last_name):
    taxrate = TAXRATE

    res = utils.select('''
    SELECT round(sum(oi.price) + COALESCE(sum(ti.price) * %(taxrate)s, 0), 2) total
    FROM (order_item oi left outer join taxable_item ti on ti.id = oi.id), order_group og
    WHERE oi.order_group_id = og.id 
    AND oi.is_cancelled = False
    AND oi.is_comped = False
    AND is_open = true
    AND og.table_id = concat(%(first_name)s,' ',%(last_name)s)
    ''', args = locals()
    )

    if res:
      return res[0]['total']
    else:
      return None

def close_staff_tab(first_name, last_name):
    utils.execute('''
      UPDATE order_group
      SET is_open = FALSE, closedby = 1, updated = curdate() + interval '4' hour #4am so it won't affect tip pool
      WHERE is_open = TRUE
      AND table_id = concat(%(first_name)s,' ',%(last_name)s)
    ''', args = locals())

    
if __name__ == '__main__':
    go()
