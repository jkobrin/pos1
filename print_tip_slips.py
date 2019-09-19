import utils
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

    slipfile = open('/var/www/tipslips/'+rec['last_name']+'_'+rec['first_name']+'_tip', 'w')
    slipfile.write(text.encode('latin1', 'replace'))
    slipfile.close()
    #utils.print_slip(text, outfile = '/tmp/'+rec['last_name']+'_'+rec['first_name']+'_tip') #, lang='html') 

  #utils.execute('''update hours set paid = true where paid = false and tip_pay is not null''');

  return json.dumps('printing %s slips' % len(tip_data))


if __name__ == '__main__':
  index(None)
    
