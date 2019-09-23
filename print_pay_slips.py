import utils, populate_pay_stub
import queries
import json
from texttab import TAXRATE
TEXTWIDTH = 25

def go():
    populate_response = populate_pay_stub.populate_pay_stub(temp = False)
    weekly_pay = queries.weekly_pay(printmode = 1)

    slip_texts = []
    for rec in weekly_pay:
      #make tip stuff empty strings if they are None
      rec['tip_detail'] = rec['tip_detail'] or ''
      rec['unpaid_tips'] = rec['unpaid_tips'] or 0
      #break 'detail' string into seperate indented lines
      rec['tip_detail'] = '  '+rec['tip_detail'].replace('|', '\n  ')

      #total payout
      rec['payout'] = rec['net_wage'] + rec['unpaid_tips']

      #modify total payout if there is an open tab
      open_tab = total_staff_tab(rec['first_name'], rec['last_name'])
      rec['open_tab'] = open_tab
      if open_tab is not None:
        if open_tab <= rec['net_wage']:
          #close_staff_tab(rec['first_name'], rec['last_name'])
          rec['open_tab'] = str(open_tab) + ' CLOSED'
          rec['payout'] = round(float(rec['payout']) - float(open_tab))
        else:
          rec['open_tab'] = str(open_tab) + ' STILL OPEN'
          
      slip_texts.append(get_slip_text(rec))

    utils.execute('''update hours set paid = true where paid = false and tip_pay is not null''');
    return json.dumps(slip_texts, cls=utils.MyJSONEncoder)


def get_slip_text(rec):
    
    text = '''
{first_name} {last_name} 
week of: {week_of}
week tips: {tips}
undisbursed tips:
{tip_detail}
  total: {unpaid_tips}
total hourly: {total_hourly_pay}
{hours_worked} hours @ {pay_rate} per hr.
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
