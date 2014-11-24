import json
import utils


def index(req, receipts_id, field_name, new_value):
  
  utils.execute(
  '''update receipts_by_server set %(field_name)s = '%(new_value)s' where id = %(receipts_id)s;'''%locals()
  )

  return json.dumps(None)


def new_record(req, person_id, dat):
    
    utils.execute(
    '''insert into receipts_by_server (id, person_id, dat, cc1, cc2, cash1, cash2) 
       values (null, "%(person_id)s", "%(dat)s", null, null, null, null);
    '''%locals()
    )
  
    results = utils.select(
    '''select id from receipts_by_server where person_id =  '%(person_id)s' and dat = '%(dat)s'; '''%locals()
    )
    
    return json.dumps(results[0]['id'])
   
if __name__ == '__main__':
  print new_record(None, 9175, "2014-02-22")

