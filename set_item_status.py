import json
import MySQLdb
import utils

#log = open('/tmp/logq', 'a')


def delivered(req, item_id):

    utils.execute('''
      UPDATE order_item oi
      set oi.is_delivered =TRUE, oi.updated = NOW()
      where oi.id = %(item_id)s
    ''' % locals())

    return json.dumps(None);
    

def comped(req, item_id):

    utils.execute('''
      UPDATE order_item oi
      set oi.is_comped =TRUE, oi.updated = NOW()
      where oi.id = %(item_id)s
    ''' % locals())
    
    return json.dumps(None);

if __name__ == '__main__':
  pass
