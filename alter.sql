

#alter table person add column nickname varchar(16);
#update person set nickname = 'Joe' where first_name = 'Joseph' and last_name = 'Young';
#update person set nickname = 'Josh' where first_name = 'Joshua' and last_name = 'Kobrin';
#update person set nickname = 'Jade', first_name = 'Jehbys' where first_name = 'Jade' and last_name = 'Hernandez';

#-----------------------------------------------------------

#alter table person add column salary decimal(6,2);

#update person set salary = 0, pay_rate = 0 where last_name = 'DiLemme';

#insert into employee_tax_info values(
#      null, 
#      (select id from person where first_name = 'John' and last_name = 'DiLemme'),
#      True,
#      4,
#      .392,
#      null,
#      null);
#

#alter table winelist add column subcategory varchar(32);

#create or replace view winelist_inv as 
#select wl.*, units_in_stock - sum(IF(oi.menu_item_id is null, 0, IF(oi.item_name like 'qt:%', .25, 1))) as estimated_units_remaining, (select count(*) from revenue_item ri where ri.menu_item_id = oi.menu_item_id and ri.created > now() - interval '1' week) as weeksold
#from winelist wl left outer join order_item oi on
#wl.inventory_date <= oi.created
#and oi.menu_item_id = wl.id 
#and (oi.is_cancelled is null or oi.is_cancelled = false)
#where wl.active = true 
#group by wl.id;
#



#create or replace view active_wine
#as
#select * from winelist 
# where ((`winelist`.`active` = 1) and (`winelist`.`category` is not null) and (`winelist`.`listprice` <> 0) and (`winelist`.`listprice` is not null) and (`winelist`.`bin` is not null));
#
#alter table order_item add column taxable boolean not null;
#
#create or replace view revenue_item as select oi.* from order_item oi, order_group og 
#where oi.order_group_id = og.id
#and is_comped = false 
#and is_cancelled = false 
#and item_name not like 'gift%' 
#and og.table_id not rlike '[A-Z][a-z]+ [A-Z][a-z]+;'
#;

#create or replace view taxable_item as select * from revenue_item where taxable = true;


#
#CREATE TABLE client_session (
#  id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
#  created TIMESTAMP DEFAULT NOW()
#) ENGINE=MyISAM; 
#
#ALTER TABLE client_session AUTO_INCREMENT = 2500;

#alter table order_item add column taxable boolean not null;

#alter table order_item add column category varchar(64);
#alter table order_item add column subcategory varchar(64);
#alter table order_item add column parent_item INT;

create or replace view revenue_item as select oi.* from order_item oi, order_group og 
where oi.order_group_id = og.id
and is_comped = false 
and is_cancelled = false 
and item_name not like 'gift%' 
and og.table_id not rlike '[A-Z][a-z]+ [A-Z][a-z]+';

create or replace view taxable_item as select * from revenue_item where taxable = true;

#alter table hours add column paid boolean default false;
#update hours set paid = true where tip_pay is not null;
#alter table hours modify column intime timestamp default now();
#alter table hours modify column tip_pay DECIMAL(3,0) default null;

#alter table order_item add column fraction float default 1;

#drop table sku;

#CREATE TABLE sku (
#  id int NOT NULL AUTO_INCREMENT,
#  name varchar(64),
#  supercategory varchar(32),
#  category varchar(32),
#  subcategory varchar(32),
#  retail_price float,
#  qtprice float,
#  add_on boolean default False,
#  scalable boolean default False,
#  tax varchar(16),
#  wholesale_price float,
#  supplier varchar(64),
#  vendor_code varchar(8),
#  bin varchar(4),
#  listorder int,
#  upc varchar(16),
#  description varchar(1024),
#  active boolean default true,
#  units_in_stock int(4) DEFAULT '0',
#  inventory_date date default 0,
#  mynotes varchar(256),
#  PRIMARY KEY (`id`)
#)ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
#
#
#alter table order_group add column paid_before_close boolean default false;

alter table order_group add column pickup_time timestamp null default null;

alter table sku add column display_name varchar(64) null default null;

alter table sku add column extra varchar(1024) null default null;

