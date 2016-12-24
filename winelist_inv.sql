create or replace view winelist_inv as 
select wl.*, units_in_stock - sum(IF(oi.menu_item_id is null, 0, IF(oi.item_name like 'qt:%', .25, 1))) as estimated_units_remaining
from winelist wl left outer join order_item oi on
wl.inventory_date <= oi.created
and oi.menu_item_id = wl.id 
and (oi.is_cancelled is null or oi.is_cancelled = false)
where wl.active = true 
group by wl.id;

