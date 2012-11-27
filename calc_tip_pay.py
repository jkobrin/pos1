
import json
import MySQLdb
import utils


def index(req, the_tip, lag_days):

  utils.execute(
    '''
    create or replace view person_hours_items
    as
    select si.id as si_id, si.price, h.tip_share, h.id as h_id, h.person_id
    from 
      served_item si
      ,hours h
    where si.created between h.intime and h.outtime
      and DATE(si.created- INTERVAL '4' HOUR) =  DATE(NOW()) - INTERVAL '%(lag_days)s' DAY 
      and (time(si.created) > '16:00:00' or time(si.created) < '04:00:00')
    '''%locals()
  )

  utils.execute(
    '''
    create or replace view item_split
    as
    select si_id, price / sum(tip_share) split_price from person_hours_items group by si_id; 
    '''
  )

  utils.execute(
  '''
  create or replace view tip_pay
  as
  select
    p.last_name, 
    phi.h_id,
    sum(split_price)/(select total from night_tots where dat = DATE(NOW()) - INTERVAL '%(lag_days)s' DAY) * %(the_tip)s * tip_share as tip
  from 
  item_split spl
  ,person_hours_items phi
  ,person p
  where spl.si_id = phi.si_id
  and p.id = phi.person_id
  group by phi.h_id;
  '''%locals()
  )

  utils.execute('''
  update hours h inner join tip_pay tp on h.id = tp.h_id set h.tip_pay = tp.tip;
  '''
  )

  return json.dumps(0)

if __name__ == '__main__':
  print index(None)
