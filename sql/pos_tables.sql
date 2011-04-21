
drop table order_group;

CREATE TABLE order_group (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  table_id VARCHAR(3) NOT NULL,
  is_open boolean NOT NULL DEFAULT TRUE,
  closedby INT,
  created TIMESTAMP DEFAULT NOW(),
  FOREIGN KEY (closedby) REFERENCES person(id) ON DELETE CASCADE
);


drop table order_item;

CREATE TABLE order_item (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  order_group_id INT NOT NULL,
  item_name VARCHAR(32) NOT NULL,
  price FLOAT NOT NULL,
  is_cancelled BOOLEAN NOT NULL DEFAULT FALSE,
  is_delivered BOOLEAN NOT NULL DEFAULT FALSE,
  is_comped BOOLEAN NOT NULL DEFAULT FALSE,
  created TIMESTAMP DEFAULT NOW(),
  updated TIMESTAMP DEFAULT 0,
  INDEX order_idx (order_group_id),
  FOREIGN KEY (order_group_id) REFERENCES order_group(id) ON DELETE CASCADE
);


drop table person;

CREATE TABLE person (
  id INT NOT NULL PRIMARY KEY,
  first_name VARCHAR(32) NOT NULL,
  last_name VARCHAR(32) NOT NULL,
  created TIMESTAMP DEFAULT NOW(),
  updated TIMESTAMP DEFAULT 0
);


drop table hours;

CREATE TABLE hours (
  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  person_id INT NOT NULL,
  intime TIMESTAMP DEFAULT 0,
  outtime TIMESTAMP DEFAULT 0,
  INDEX person_idx (person_id),
  FOREIGN KEY (person_id) REFERENCES person(id) ON DELETE CASCADE
);

CREATE or REPLACE view hours_worked as
select 
  intime,
  date_format(intime,"%m/%d") as date,
  last_name, 
  date_format(intime, "%H:%i") time_in, 
  date_format(outtime, "%H:%i") time_out, 
  hour(timediff(outtime, intime)) + minute(timediff(outtime, intime))/60 hours_worked 
from 
  hours h, 
  person p 
  where h.person_id = p.id;

