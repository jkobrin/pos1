set @the_tip = 233.3;

create or replace view last_night_items
as
select * from order_item
where is_cancelled = False
  and item_name not like 'gift%'
  and DATE(created- INTERVAL '8' HOUR) =  DATE(NOW()) - INTERVAL '1' DAY
  #and DATE(created- INTERVAL '8' HOUR) =  '2012-1-18'
;

create or replace view person_items
as
select lni.id as lni_id, lni.price, p.id as p_id, last_name
  , if(p.last_name = 'Barbagallo', 0,
    if(p.last_name = 'Norman', 1, 
    if(p.last_name = 'Addy', .5, 
    if(p.last_name = 'Smith', .5, 
    if(p.last_name = 'x', 1.7, 
        1)))))person_share
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

select '--------',dayname(min(created)), date(min(created)),'------------' from last_night_items;
select last_name, round(sum(split_price)/(select sum(price) from last_night_items) * @the_tip * person_share)
from 
  item_split spl
  ,person_items pi
where spl.lni_id = pi.lni_id
and person_share !=0
group by pi.p_id;

select 'total', round(@the_tip) from dual;
