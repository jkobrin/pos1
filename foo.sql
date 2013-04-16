create or replace view qtinos_sold as 
select wl.id, count(*) qsold 
from winelist wl, order_item oi 
where wl.active = true 
and wl.inventory_date <= oi.created
and oi.is_cancelled = false
and oi.item_name like CONCAT('qt:%', substring(wl.name, 1, 22), '%') 
group by wl.id;

create or replace view btls_sold as 
select wl.id, count(*) bsold 
from winelist wl, order_item oi 
where wl.active = true 
and wl.inventory_date <= oi.created
and oi.is_cancelled = false
and oi.item_name not like 'qt:%'
and oi.item_name like CONCAT('%', substring(wl.name, 1, 22), '%') 
group by wl.id;


create or replace view wine_sold_since_inventory as
select wl.*, IFNULL(qs.qsold,0) qsold, IFNULL(bs.bsold, 0) bsold
from winelist wl left join qtinos_sold qs on (wl.id = qs.id) left join btls_sold bs on (wl.id =bs.id)
where active = true;

create or replace view wine_inventory as
select wssi.*, units_in_stock - bsold - qsold /4 as estimated_current_units 
from wine_sold_since_inventory wssi
where active = true;

