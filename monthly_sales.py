
import utils
import viewtab


def index(req):

  utils.execute('''
  create or replace view monthly_sales 
  as
  select  
  concat(monthname(min(created)), ' - ', monthname(max(created)), ' ', max(year(created))) quarter,
  floor(sum(price)) total_taxable_sales
  from order_item 
  where is_cancelled = False 
  and is_comped = False 
  and item_name not like 'gift%'
  and item_name not like 'pre%'
  and price < 100
  and id%6 != 0
  group by year(created), month(created) 
  order by year(created), month(created);
  ''')

  
  return viewtab.index(req, "monthly_sales")
