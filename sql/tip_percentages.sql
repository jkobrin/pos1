set @the_tip = 173;

create or replace view last_night_items
as
select * from order_item
where is_cancelled = False
  and item_name not like 'gift%'
  and created > now() - INTERVAL '24' HOUR
  #and date(created- interval '8' hour) =  '2012-1-11'
;

create or replace view person_items
as
select lni.id as lni_id, lni.price, p.id as p_id, last_name
  , if(p.last_name = 'Barbagallo', 0,
    if(p.last_name = 'Smith', .5, 
    if(p.last_name = 'Addy', .5, 
        1)))person_share
from 
  last_night_items lni
  ,hours h
  ,person p
where h.person_id = p.id
  and lni.created between h.intime and if(h.outtime=0, h.intime + interval '12' hour, h.outtime)
;

create or replace view item_split
as
select lni_id, price / sum(person_share) split_price from person_items group by lni_id; 


select last_name, sum(split_price)/(select sum(price) from last_night_items) * @the_tip * person_share
from 
  item_split spl
  ,person_items pi
where spl.lni_id = pi.lni_id
group by pi.p_id;
