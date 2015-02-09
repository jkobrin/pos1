CREATE or REPLACE view hours_worked as
select 
  p.last_name, p.first_name, p.pay_rate, p.weekly_tax,
  p.id as person_id,
  intime,
  date_format(intime,"%m/%d") as date,
  date_format(intime, "%H:%i") time_in, 
  date_format(outtime, "%H:%i") time_out, 
  hour(timediff(outtime, intime)) + minute(timediff(outtime, intime))/60 hours_worked,
  h.tip_pay 
from 
  hours h, 
  person p 
  where h.person_id = p.id;

