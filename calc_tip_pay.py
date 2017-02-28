
import json
import MySQLdb
import utils


def index(req, the_tip, lag_days):

  cursor = utils.get_cursor()

  last_night_items_query = (
    '''
    create temporary table last_night_items
    as
    select si.*
    from 
      served_item si,
      order_group
    where si.order_group_id = order_group.id 
    and (order_group.table_id not rlike '^M|Couch' or time(si.created) > '16:00:00')
    and DATE(si.created- INTERVAL '4' HOUR) =  DATE(NOW()) - INTERVAL '%(lag_days)s' DAY 
    '''
  )

  utils.execute(
    last_night_items_query %locals(), cursor
  )

  utils.execute(
    '''
    create temporary table person_hours_items
    as
    select si.id as si_id, si.price, h.tip_share, h.id as h_id, h.person_id,
    IF(h.tip_share >=.8, 'FOH', 'BOH') pool_group
    from 
      last_night_items si
      ,hours h
    where si.created between h.intime and ifnull(h.outtime, now())
    '''%locals(), cursor
  )

  utils.execute(
    '''
    create temporary table item_split
    as
    select si_id, pool_group, price * IF(pool_group = "FOH", .62, .38) / sum(tip_share) split_price 
    from person_hours_items  
    group by si_id, pool_group; 
    ''', cursor
  )

  utils.execute(
  '''
  create temporary table tip_pay
  as
  select
    p.last_name, 
    phi.h_id,
    sum(split_price)/(select sum(price) from last_night_items) * %(the_tip)s * tip_share as tip
  from 
  item_split spl
  ,person_hours_items phi
  ,person p
  where spl.si_id = phi.si_id
  and p.id = phi.person_id
  and phi.pool_group = spl.pool_group
  group by phi.h_id;
  '''%locals(), cursor
  )

  utils.execute('''
  update hours h inner join tip_pay tp on h.id = tp.h_id set h.tip_pay = tp.tip, h.paid = false;
  ''', cursor
  )

  return json.dumps(0)

if __name__ == '__main__':
  print index(None)
