
import queries
import texttab
import json


def index(req, lag_days):  
  hours =  queries.hours(lag_days=lag_days)

  return json.dumps(hours)


if __name__ == '__main__':
  print index(None, 1)
