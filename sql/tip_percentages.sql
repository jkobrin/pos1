#TODO: exclude lunch the following day
set @the_tip = 620.48;

create or replace view last_night_items
as
select * from order_item
where is_cancelled = False
  and item_name not like 'gift%'
  and DATE(created- INTERVAL '4' HOUR) =  DATE(NOW()) - INTERVAL '1' DAY 
  and (time(created) > '16:00:00' or time(created) < '04:00:00')
;

create or replace view person_items
as
select lni.id as lni_id, lni.price, p.id as p_id, last_name
  , if(p.last_name = 'Kobrin', .7,
    if(p.last_name = 'Pampalone', 1, 
    if(p.last_name = 'Ponce', 1, 
    if(p.last_name = 'Smith', .5,
    if(p.last_name = 'Labossier', 1,
    if(p.last_name = 'Salazar', 1, 
    if(p.last_name = 'Lilli', 1,
    if(p.last_name = 'Young', 1,
    if(p.last_name = 'DiLemme', 1, 
    if(p.last_name = 'Addy', 0, 
        1))))))))))person_share
from 
  last_night_items lni
  ,hours h
  ,person p
where h.person_id = p.id
  and lni.created between h.intime and h.outtime
;

create or replace view item_split
as
select lni_id, price / sum(person_share) split_price from person_items group by lni_id; 

select '--------',dayname(min(created)), date(min(created)),'------------*(not yet paid out)' from last_night_items;
select last_name, round(sum(split_price)/(select sum(price) from last_night_items) * @the_tip * person_share)
from 
  item_split spl
  ,person_items pi
where spl.lni_id = pi.lni_id
and person_share !=0
group by pi.p_id;

select 'total', round(@the_tip) from dual;
