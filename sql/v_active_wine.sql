

create or replace view active_wine 
as 
select * from winelist
where active = true
and category is not null
and listprice <> 0
and listprice is not null
and bin is not null
;
