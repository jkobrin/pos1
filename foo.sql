 #Field        | Type         | Null | Key | Default             | Extra |
 #+--------------+--------------+------+-----+---------------------+-------+
 #| last_name    | varchar(32)  | NO   |     | NULL                |       |
 #| first_name   | varchar(32)  | NO   |     | NULL                |       |
 #| pay_rate     | float        | NO   |     | 8                   |       |
 #| weekly_tax   | float        | NO   |     | 0                   |       |
 #| salary       | decimal(6,2) | YES  |     | NULL                |       |
 #| person_id    | int(4)       | NO   |     | 0                   |       |
 #| intime       | timestamp    | NO   |     | 0000-00-00 00:00:00 |       |
 #| date         | varchar(5)   | YES  |     | NULL                |       |
 #| time_in      | varchar(10)  | YES  |     | NULL                |       |
 #| time_out     | varchar(10)  | YES  |     | NULL                |       |
 #| hours_worked | decimal(6,4) | YES  |     | NULL                |       |
 #| tip_pay      | decimal(3,0) | YES  |     | NULL                |       |
 #+--------------+--------------+------+-----+---------------------+-------+


select 
  last_name, 
  first_name, 
  pay_rate, 
  weekly_tax, 
  salary, 
  id as person_id, 
  (now() - interval '1' week) as intime, 
  (now() - interval '1' week) as date,
  (now() - interval '1' week) as time_in,
  (now() - interval '1' week) as time_out,
  0 as hours_worked,
  0 as tip_pay
from person where salary > 0;  

