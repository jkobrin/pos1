import utils

def index(req):

  tip_slips_query = (
    '''
    select 
      person.first_name, 
      person.last_name,
      sum(tip_pay) as total_tips,
      group_concat(concat_ws(' - $', date_format(intime, '%a %b %D'), tip_pay) SEPARATOR '|') as detail
    from 
    hours join person on hours.person_id = person.id
    where date(hours.intime) >= (select date(max(created)) from tip_slips_printed)
    and hours.tip_pay is not null
    group by person.id
    order by person.last_name, person.first_name
    '''
  )

  tip_data = utils.select(tip_slips_query)

  for rec in tip_data:

    text = '''
    {first_name} {last_name}'''.format(**rec)
    for det in rec['detail'].split('|'):
      text += '''
    %s'''%det  
    text +=''' 
    TOTAL: ${total_tips}
    '''.format(**rec)

    print text
    #utils.print_slip(text, outfile = '/tmp/'+rec['last_name']+'_tip.ps') 




if __name__ == '__main__':
  index(None)
    
