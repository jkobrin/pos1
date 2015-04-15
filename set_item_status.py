import json
import MySQLdb
import utils

#log = open('/tmp/logq', 'a')


def delivered(req, item_id):

    utils.execute('''
      UPDATE order_item oi
      set oi.is_delivered = NOT oi.is_delivered, oi.is_held = FALSE, oi.updated = NOW()
      where oi.id = %(item_id)s
    ''' % locals())

    return json.dumps(None);
    

def toggle_held(req, item_id):

    utils.execute('''
      UPDATE order_item oi
      set oi.is_held = NOT oi.is_held, oi.updated = NOW()
      where oi.id = %(item_id)s
    ''' % locals())

    return json.dumps(None);
    

def comped(req, item_id):

    utils.execute('''
      UPDATE order_item oi
      set oi.is_comped = NOT oi.is_comped
      where oi.id = %(item_id)s
    ''' % locals())
    
    return json.dumps(None);

if __name__ == '__main__':
  pass
