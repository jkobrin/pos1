import json
import MySQLdb
from xml.sax.saxutils import escape
import os, subprocess
import re
import utils
import datetime
import tax
from random import randint
import config_loader


def get_stub_data(person_id, week_of, table_name, incursor):  

  print person_id, week_of
  stub_data = utils.select('''
    select 
    stub.last_name as LAST_NAME,
    stub.first_name as FIRST_NAME,
    coalesce(person.ssn, "") as SOCIAL,
    coalesce(person.street_address, "") as ADDRESS,
    week_of + interval '1' week as PERIOD_END,
    concat(week_of, ' - ', week_of + interval '6' day) as PERIOD_SPAN,
    fed_withholding as FED,
    social_security_tax as SOC,
    medicare_tax as MED,
    nys_withholding as STATE,
    gross_wages as GROSS,
    gross_wages - fed_withholding - social_security_tax - medicare_tax - nys_withholding as NET,
    round(gross_wages / stub.pay_rate,2) as HOURS,
    stub.pay_rate as RATE
    from {table_name} stub join person on stub.person_id = person.id
    where person_id = {person_id}
    and week_of = "{week_of}"
  '''.format(**locals()), incursor
  )

  stub_ytd_data = utils.select('''
    select 
    sum(fed_withholding) as FEDYTD,
    sum(social_security_tax) as SOCYTD,
    sum(medicare_tax) as MEDYTD,
    sum(nys_withholding) as STATEYTD,
    sum(gross_wages) as GYTD,
    sum(gross_wages - fed_withholding - social_security_tax - medicare_tax - nys_withholding) as NETYTD
    from {table_name}
    where person_id = {person_id}
    and year("{week_of}" + interval '1' week) = year(week_of+interval '1' week) 
    and week_of <= date("{week_of}")
  '''.format(**locals()), incursor
  )

  # make one dictionary of the two result sets
  result = stub_data[0] # start with stub_data
  result.update(stub_ytd_data[0]) #add the YTD stuff to it
  result["BUSS_INFO_LINE"] = '<br>'.join(config_loader.get_config_dict()['paystub_buss_info'])

  return result


def fodt_text(stub_data):
  doc = open('/var/www/paystub_template.html').read()

  for key, value in stub_data.items():
    doc = re.sub(r'\$'+key+r'\b', str(value), doc)

  return doc


def gen_fodt_and_pdf(stub_data, table_name):
  
  doc = fodt_text(stub_data)
  stubdir = "/var/www/paystubs/"
  fodtname = stubdir + "{LAST_NAME}_{FIRST_NAME}_{PERIOD_END}".format(**stub_data)+"_{table_name}.html".format(**locals())
  new_fodt = open(fodtname, 'w')
  
  #new_fodt.write('''Subject: earnings statement {PERIOD_END}
  #To: josh@salumibarli.com
  #From: stubs@salumibarli.com
  #Content-Type: text/html

  #'''.format(**stub_data))

  new_fodt.write(doc)
  new_fodt.close()

  #os.system('soffice --headless --convert-to pdf --outdir ' + stubdir + ' ' + fodtname)
  #subprocess.call(['soffice', '-env:HOME=/tmp/libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', stubdir, fodtname])


def print_stubs(person_id, week_of, table_name, incursor = None):
  
    stub_data = get_stub_data(person_id, week_of, table_name, incursor)
    gen_fodt_and_pdf(stub_data, table_name)
    return stub_data


def print_recent(person_lastname, numweeks=6, table_name='PAY_STUB'):

    stub_keys = utils.select('''
      select person_id, week_of from %(table_name)s 
      where last_name  = '%(person_lastname)s'
      and yearweek(week_of) >= yearweek(now() - interval '%(numweeks)s' week)
    '''%locals(), label=False
    )

    print "stub_keys %s"% repr(stub_keys)
    for person_id, week_of in stub_keys:
      print (person_id, week_of)
      yield print_stubs(person_id, week_of, table_name)


def print_2016_stubs():

  for table_name in ('PAY_STUB', 'WEEKLY_PAY_STUB'):
    stub_keys = utils.select('''
      select person_id, week_of from %(table_name)s where year(week_of) = 2016
    '''%locals(), label=False
    )

    for person_id, week_of in stub_keys:
      print_stubs(person_id, week_of, table_name)


def print_one_week_stubs(week_of):

  for table_name in ('PAY_STUB', 'WEEKLY_PAY_STUB'):
    stub_keys = utils.select('''select person_id from {table_name} where week_of = {week_of}'''.format(**locals()), label=False) 

    for person_id in stub_keys:
      print_stubs(person_id, week_of, table_name)
  

def print_this_week_stubs():

  for table_name in ('WEEKLY_PAY_STUB',):# 'PAY_STUB'):
    stub_keys = utils.select('''
      select person_id, week_of from {table_name} where yearweek(week_of) = yearweek(now() - interval '2' week)'''.
      format(**locals()), label=False) 

    for person_id, week_of in stub_keys:
      yield print_stubs(person_id, week_of, table_name)
  


def last_sundays(num):
  today = datetime.date.today()
  sunday = today - datetime.timedelta(days = today.isoweekday())

  for x in xrange(num):
    sunday -= datetime.timedelta(days = 7)
    yield sunday.isoformat()


def make_estub(first_name, last_name, person_id, baserate, rate_variance, basehours, hour_variance):

  incursor = utils.get_cursor()
  table_name = 'E_STUB'
  utils.execute('''
    create temporary table E_STUB like PAY_STUB;
  ''', incursor=incursor);

  for sunday in last_sundays(7):

    hours = basehours + randint(-basehours, basehours)*hour_variance
    rate = baserate + randint(-baserate, baserate)*rate_variance
    wages = rate*hours

    row = {
      'week_of' : sunday,
      'person_id' : person_id,
      'last_name': last_name, 
      'first_name': first_name,
      'hours_worked' : hours,
      'pay_rate': rate, 
      'allowances': 1,
      'nominal_scale': 0,
      'married': 0,
      'weekly_pay': 0,
      'gross_wages': wages,
      'tips': 0,
      'total_hourly_pay': rate
    }

    tax.add_witholding_fields(row)
    columns = ', '.join(row.keys())
    values = ', '.join(("'%s'" % value for value in row.values()))
    sqltext = 'INSERT into %s (%s) VALUES (%s);'%(table_name, columns, values)
    #my_logger.debug('pay stub: ' + sqltext)
    utils.execute(sqltext, incursor=incursor)
    
  for sunday in last_sundays(2):
    yield print_stubs(person_id, sunday, table_name, incursor=incursor)

def index(req): #, lname, numweeks=6, table_name= 'PAY_STUB'):
  #allfeedback = list(make_estub('Adeliya', 'Geistrikh', 6667, 32, 0 , 40, 0))
  #allfeedback += list(make_estub('Roman', 'Geistrikh', 6668, 33, 0 , 40, 0))
  allfeedback = print_recent('Brewster', numweeks=8, table_name = 'WEEKLY_PAY_STUB')
  #allfeedback = print_recent('Russo', numweeks=12, table_name = 'WEEKLY_PAY_STUB')
  return 'THIS:' + '\n\n'.join(repr(feedback) for feedback in allfeedback)
    

if __name__ == '__main__':
  make_estub('Jonathan', 'Labossier', 2222, 35, 0 , 40, 0)
  #print_this_week_stubs()
  #print_recent('Rubio', numweeks=6, table_name = 'PAY_STUB')
  #print_recent('Fostakovska', numweeks=12, table_name = 'WEEKLY_PAY_STUB')
  #print_recent('Seney', numweeks=12, table_name = 'WEEKLY_PAY_STUB')
  #print_recent('Seney', numweeks=12, table_name = 'PAY_STUB')
  #print_recent('Graziose', numweeks=12, table_name = 'WEEKLY_PAY_STUB')
  #print_recent('Gamez', numweeks=30, table_name = 'PAY_STUB')
  #print_recent('Boccio', numweeks=6, table_name = 'PAY_STUB')
  #print_recent('Jean-Pierre', numweeks=6, table_name = 'PAY_STUB')
