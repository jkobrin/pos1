import queries
import texttab
import json


def get(req, lag_days):  
  info_by_server =  queries.nightly_sales_by_server(label=True, lag_days=lag_days)
  #server_info = {}
  #for row in info_by_server:
  #  server_info[row['server'].lower()] =  server_inf(**row)

  return json.dumps(info_by_server)


def get_new(req, lag_days):  
  info_by_server =  queries.new_sales_by_server(label=True, lag_days=lag_days)
  return json.dumps(info_by_server)


if __name__ == '__main__':
  print get()
