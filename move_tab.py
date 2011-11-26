import json
import MySQLdb
import utils

from mylog import my_logger
log = my_logger

def index(req, p_from, p_to):
  log.debug('move tab : ' + p_from + "  " + p_to)
  logy = open("/var/www/foo.log", "w")
  logy.write('move tab : ' + p_from + "  " + p_to +'\n')


  #is_to_tab_open = utils.select(
  #  '''select 1
  #     from order_group og
  #     where og.table_id = "%(p_to)s"
  #     and og.is_open = true''' % locals()
  #)

  #if not is_to_tab_open:
  utils.execute(
    '''update order_group og
      set table_id = "%(p_to)s"
      where table_id = "%(p_from)s"
      and og.is_open = true'''% locals()
  )    

  return json.dumps(None)


if __name__ == '__main__':
  print index(None)
