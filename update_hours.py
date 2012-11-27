
import utils


def index(req, hours_id, field_name, new_value):
  
  utils.execute(
  '''update hours set %(field_name)s = '%(new_value)s' where id = %(hours_id)s'''%locals()
  )
