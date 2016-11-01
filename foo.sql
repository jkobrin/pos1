insert into reopened
select null, '192.168.1.27', null, closedby, id
from order_group
where id in (38696);
