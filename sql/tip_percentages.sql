#TODO: exclude lunch the following day
#07/15
#Labossier --  cash:528.0   credit:0   sales:369.37375   credit tips:0   cash tips:158.62625   all tips:158.62625  tip%: 58.5336715867
#Salazar --  cash:1115.0   credit:0   sales:928.74375   credit tips:0   cash tips:186.25625   all tips:186.25625  tip%: 21.7843567251
#all tips: 344.8825

#07/16
#Lilli --  cash:579.87   credit:0   sales:474.69125   credit tips:0   cash tips:105.17875   all tips:105.17875  tip%: 24.0683638444
#Young --  cash:350.0   credit:0   sales:326.96125   credit tips:0   cash tips:23.03875   all tips:23.03875  tip%: 7.65406976744
#Ponce --  cash:67.0   credit:0   sales:51.05375   credit tips:0   cash tips:15.94625   all tips:15.94625  tip%: 33.9281914894
#all tips: 144.16375
#ADJUST YOUNGS TIPS
#Server last name: Y   
#Young --  cash:350.0   credit:0   sales:326.96125   credit tips:0   cash tips:23.03875   all tips:23.03875  tip%: 7.65406976744
#collected: 60
#Young --  cash:410.0   credit:0   sales:326.96125   credit tips:0   cash tips:83.03875   all tips:83.03875  tip%: 27.5876245847
#Server last name: 
#Lilli --  cash:579.87   credit:0   sales:474.69125   credit tips:0   cash tips:105.17875   all tips:105.17875  tip%: 24.0683638444
#Young --  cash:410.0   credit:0   sales:326.96125   credit tips:0   cash tips:83.03875   all tips:83.03875  tip%: 27.5876245847
#Ponce --  cash:67.0   credit:0   sales:51.05375   credit tips:0   cash tips:15.94625   all tips:15.94625  tip%: 33.9281914894
#all tips: 204.16375



set @the_tip = 525.57;

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
  , if(p.last_name = 'Kobrin', .0,
    if(p.last_name = 'Pampalone', 1, 
    if(p.last_name = 'Ponce', .5, 
    if(p.last_name = 'Smith', .5,
    if(p.last_name = 'Labossier', 1,
    if(p.last_name = 'Salazar', 1.0, 
    if(p.last_name = 'Lilli', 1.0,
    if(p.last_name = 'Young', 1.2, 
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
