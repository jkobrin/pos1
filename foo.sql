create or replace view winelist_w_sold as 
select wl.*, units_in_stock - sum(IF(oi.item_name like 'qt:%', .25, 1)) as estimated_units_remaining
from winelist wl, order_item oi 
where wl.active = true 
and wl.inventory_date <= oi.created
and oi.menu_item_id = wl.id
and oi.is_cancelled = false
group by wl.id;


/*
create or replace view wine_sold_since_inventory as
select wl.*, IFNULL(qs.qsold,0) qsold, IFNULL(bs.bsold, 0) bsold
from winelist wl left join qtinos_sold qs on (wl.id = qs.id) left join btls_sold bs on (wl.id =bs.id)
where active = true;

create or replace view wine_inventory as
select wssi.*, units_in_stock - bsold - qsold /4 as estimated_current_units 
from wine_sold_since_inventory wssi
where active = true;
*/
