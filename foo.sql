drop table if exists receipts_by_server;

CREATE TABLE receipts_by_server (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  person_id INT not null,
  dat date not null,
  cc1 float,
  cc2 float,
  cash1 float,
  cash2 float,
  INDEX rbs_person_id (person_id),
  INDEX rbs_dat (dat),
  FOREIGN KEY (person_id) REFERENCES person(id) ON DELETE CASCADE
)

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

