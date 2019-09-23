import utils, queries
import json


def index(req):

  tip_slips_query = (
    '''
    select 
      person.last_name,
      person.first_name, 
      sum(tip_pay) as total_tips,
      group_concat(concat_ws(' - $', date_format(intime, '%a %b %D'), tip_pay) SEPARATOR '|') as detail
    from 
    hours join person 
    on hours.person_id = person.id
    where hours.paid = false
    and hours.tip_pay is not null
    group by person.id
    order by person.last_name, person.first_name
    '''
  )

  tip_records = utils.select(tip_slips_query)
  for record in tip_records: 
    #break 'detail' string into a list of seperate string objects
    record['detail'] = record['detail'].split('|')

  #utils.execute('''update hours set paid = true where paid = false and tip_pay is not null''');

  return json.dumps(tip_records))


if __name__ == '__main__':
  index(None)
    
