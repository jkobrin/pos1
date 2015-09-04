
SELECT 
      concat(p.last_name, ', ', substr(p.first_name,1,1), '.') server,
      p.id as person_id,
      p.ccid,
      sum(oi.price) sales, 
      sum(ti.price) taxable_sales,
      sum(oi.price) + COALESCE(round(sum(ti.price) * .08625, 2),0) receipts,
      count(distinct og.id) tabs_closed,
      convert(date(now() - INTERVAL '0' DAY), CHAR(10)) as dat
    FROM (order_item oi left outer join taxable_item ti on ti.id = oi.id), order_group og, person p 
    WHERE oi.order_group_id = og.id 
    AND oi.is_cancelled = False
    AND oi.is_comped = False
    AND og.closedby = p.id 
    AND date(og.updated - interval '6' HOUR) = date(now() - INTERVAL '0' DAY)
    GROUP BY p.id
