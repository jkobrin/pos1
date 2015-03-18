

#alter table person add column nickname varchar(16);
#update person set nickname = 'Joe' where first_name = 'Joseph' and last_name = 'Young';
#update person set nickname = 'Josh' where first_name = 'Joshua' and last_name = 'Kobrin';
#update person set nickname = 'Jade', first_name = 'Jehbys' where first_name = 'Jade' and last_name = 'Hernandez';

#-----------------------------------------------------------

alter table person add column salary decimal(6,2);

update person set salary = 1530, pay_rate = 0 where last_name = 'DiLemme';

insert into employee_tax_info values(
      null, 
      (select id from person where first_name = 'John' and last_name = 'DiLemme'),
      True,
      4,
      .392,
      null,
      null);


CREATE or REPLACE view hours_worked as
select 
  p.last_name, p.first_name, p.pay_rate, p.weekly_tax, p.salary,
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


create or replace view pstub_with_week_ending
as
select week_of + interval '6' DAY as week_ending, PAY_STUB.* from PAY_STUB
;

create or replace view monthly_withholding
as
select concat(min(week_of), ' - ', max(week_of)) weeks_of, 
first_name, 
last_name, 
sum(gross_wages) gross_wages,
sum(fed_withholding) fed_withholding,
sum(nys_withholding) nys_withholding,
sum(medicare_tax) medicare_tax,
sum(social_security_tax) social_security_tax
from pstub_with_week_ending
where nominal_scale != 0
group by person_id, 
year(week_ending), 
month(week_ending);
