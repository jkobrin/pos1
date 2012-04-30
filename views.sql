
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
