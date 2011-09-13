create or replace view last_night_items
as
select * from order_item
where is_cancelled = False
  and created > now() - INTERVAL '24' HOUR
;

create or replace view person_items
as
select lni.id as lni_id, lni.price, p.id as p_id, last_name
from 
  last_night_items lni
  ,hours h
  ,person p
where h.person_id = p.id
  and lni.created between h.intime and h.outtime
;

create or replace view item_split
as
select lni_id, price / count(p_id) split_price from person_items group by lni_id; 


select sum(split_price)/(select sum(price) from last_night_items), p_id, last_name
from 
  item_split spl
  ,person_items pi
where spl.lni_id = pi.lni_id
group by pi.p_id;
