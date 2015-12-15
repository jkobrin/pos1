select
      og.table_id, oi.updated,
      oi.id, oi.is_delivered, oi.is_held, oi.is_comped, oi.price,
      TIMESTAMPDIFF(MINUTE, oi.created, now()) minutes_old,
      TIMESTAMPDIFF(MINUTE, oi.updated, now()) minutes_since_mod,
      TIMESTAMPDIFF(SECOND, oi.updated, now()) seconds_since_mod
    FROM order_group og, order_item oi 
    where og.id = oi.order_group_id
    and og.is_open = TRUE
    and oi.is_cancelled = FALSE;
