CREATE or REPLACE view hours_worked as
select 
  p.last_name, p.first_name, p.pay_rate, p.weekly_tax,
  intime,
  date_format(intime,"%m/%d") as date,
  date_format(intime, "%H:%i") time_in, 
  date_format(outtime, "%H:%i") time_out, 
  hour(timediff(outtime, intime)) + minute(timediff(outtime, intime))/60 hours_worked 
from 
  hours h, 
  person p 
  where h.person_id = p.id;


create or replace view served_item as select * from order_item where is_cancelled = false and item_name not like 'gift%';

create or replace view revenue_item as select * from order_item where is_comped = false and is_cancelled = false and item_name not like 'gift%';

create or replace view sales_by_week
as
select sum(price) total, year(created) year, week(created) week
from
revenue_item
group by year(created), week(created)
;



create or replace view night_tots
as
SELECT sum(price) total, dayname(og.created) dname, date(og.created) dat
FROM revenue_item oi, order_group og
WHERE oi.order_group_id = og.id 
and (time(og.created) not between '06:00:00' and '16:00:00')
group by date(og.created - INTERVAL '6' HOUR);

create or replace view day_tots
AS
SELECT sum(price) total, dayname(og.created) dname, date(og.created) dat
FROM revenue_item oi, order_group og
WHERE oi.order_group_id = og.id 
and (time(og.created) between '06:00:00' and '16:00:00')
group by date(og.created);

create or replace view nd_tots
as
SELECT nt.*, dt.total as dtotal from
(night_tots nt left outer join day_tots dt on nt.dat = dt.dat)
union
SELECT nt.total, dt.dname, dt.dat, dt.total as dtotal from
(day_tots dt left outer join night_tots nt on nt.dat = dt.dat)
;

create or replace view comped_food
as
select sum(if(is_comped = true, price, 0)) total, date(created - interval '4' hour) dat
from order_item
where item_name not rlike "([0-9]+ )|(pint )|flight|cktail"
and is_cancelled = false
group by date(created - interval '4' hour)
;


create or replace view comped_booze
as
select sum(if(is_comped = true, price, 0)) total, date(created - interval '4' hour) dat
from order_item
where item_name rlike "([0-9]+ )|(pint )|flight|cktail"
and is_cancelled = false
group by date(created - interval '4' hour)
;


create or replace view wine_tots
as
select sum(price) total, date(created - interval '4' hour) dat
from revenue_item
where item_name rlike "([0-9]+ )|(pint )|flight|cktail"
group by date(created - interval '4' hour)
;


create or replace view fw_tots
as
select wt.total wine_tot, nt.total n_tot, round(100*wt.total/nt.total,1) as wine_pct, nt.dname dname, nt.dat dat
from wine_tots wt, night_tots nt
where wt.dat = nt.dat
;

create or replace view who_worked
as
select date(intime) dat, group_concat(p.last_name) ppl
from hours h, person p where p.id = h.person_id 
group by date(intime)
;

create or replace view fw_tots_and_staff
as
select cb.total comped, fw.*, substr(ww.ppl,1, 80) ppl
from fw_tots fw, who_worked ww, comped_booze cb
where fw.dat = ww.dat
and fw.dat = cb.dat
;

create or replace view qtinos_sold as select wl.name, count(*) qsold 
from winelist wl, order_item oi where wl.active = true 
and oi.item_name like CONCAT('qt:%', substring(wl.name, 1, 22), '%') 
group by wl.id;

create or replace view liquor_sales_by_month
as
select sum(price) total, year(created), month(created)
from revenue_item
where item_name rlike "([0-9]+ )|(^qt:)|(pint )|flight|cktail|cosmo|vodka"
group by year(created), month(created)
;


create or replace view winelist_inv as 
select wl.*, units_in_stock - sum(IF(oi.menu_item_id is null, 0, IF(oi.item_name like 'qt:%', .25, 1))) as estimated_units_remaining
from winelist wl left outer join order_item oi on
wl.inventory_date <= oi.created
and oi.menu_item_id = wl.id 
and (oi.is_cancelled is null or oi.is_cancelled = false)
where wl.active = true 
group by wl.id;

