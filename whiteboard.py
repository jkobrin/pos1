
import json
import utils

from config_loader import set_newconfig_time_now

def index(req, newcontent):

  utils.execute('''update whiteboard set content = %s, updated = now()''', args=(newcontent,))
  set_newconfig_time_now()
  return json.dumps("done.")

def get_content():
  cursor = utils.get_cursor()
  cursor.execute('''select content from whiteboard''')
  row = cursor.fetchone()
  cursor.close()
  if row:
    return row[0]
  
  return 'Nothing to see here. Move along.'



