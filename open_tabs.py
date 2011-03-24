
import json
import MySQLdb
import utils


def index(req):

  open_tabs = utils.select(
    '''select 
        og.table_id,
        (select count(*) from order_item oi 
          where oi.order_group_id = og.id and is_cancelled = FALSE and is_delivered = FALSE
        ) as undelivered
        from order_group og
        where og.is_open = TRUE'''
  )

  #open_tabs = [row['table_id'] for row in open_tabs]

  return json.dumps(open_tabs)


if __name__ == '__main__':
  print index(None)
