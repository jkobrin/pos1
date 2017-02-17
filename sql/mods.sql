#alter table order_item add column is_held boolean not null default FALSE;

alter table order_group add column updated timestamp default 0;


