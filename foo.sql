select order_group.table_id, si.item_name, time(si.created), si.created
from 
served_item si,
order_group
where si.order_group_id = order_group.id 
and (order_group.table_id not rlike '^M|Couch' or time(si.created) > '16:00:00')
and DATE(si.created- INTERVAL '4' HOUR) =  DATE(NOW()) - INTERVAL '%(lag_days)s' DAY ;
