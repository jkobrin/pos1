import json
import MySQLdb
import utils


def index(req, pin):

  results = utils.select(
    '''select count(*) as cnt from person 
        where id = %s''', args=[pin]
  )

  is_good = results[0]['cnt'] != 0

  return json.dumps(is_good)


if __name__ == '__main__':
  print index(None)
