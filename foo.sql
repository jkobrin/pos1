#alter table order_item add column menu_item_id int;
#create index oi_mii_idx on order_item(menu_item_id);

create or replace view winelist_inv as 
select wl.*, units_in_stock - sum(IF(oi.menu_item_id is null, 0, IF(oi.item_name like 'qt:%', .25, 1))) as estimated_units_remaining
from winelist wl left join order_item oi on
wl.inventory_date <= oi.created
and oi.menu_item_id = wl.id 
where wl.active = true 
and (oi.is_cancelled is null or oi.is_cancelled = false)
group by wl.id;

