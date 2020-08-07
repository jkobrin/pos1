import json
import MySQLdb
import utils

from mylog import my_logger
log = my_logger

def index(req, p_from, p_to):
  # What does the 'p' stand for in these argument names? parameter?
  # I have no recollection.
  log.debug('move tab : ' + p_from + "  " + p_to)

  utils.execute(
    '''update order_group
      set table_id = %s, updated = now()
      where table_id = %s
      and is_open = true''', args=[p_to, p_from]
  )    

  return json.dumps(None)


if __name__ == '__main__':
  print index(None)
