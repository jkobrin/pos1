create or replace view winelist_inv_pure as 
select wl.*, units_in_stock - sum(IF(oi.menu_item_id is null, 0, IF(oi.item_name like 'qt:%', .25, 1))) as estimated_units_remaining, (select count(*) from revenue_item ri where ri.menu_item_id = oi.menu_item_id and ri.created > now() - interval '1' week) as weeksold
from winelist wl left outer join order_item oi on
wl.inventory_date <= oi.created
and oi.menu_item_id = wl.id 
and (oi.is_cancelled is null or oi.is_cancelled = false)
where wl.active = true 
group by wl.id;

