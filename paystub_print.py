import json
import MySQLdb
from xml.sax.saxutils import escape
from datetime import date
import os, subprocess
import re
import utils


def get_stub_choices(req):  
  
  stub_choices = utils.select('''
    select ps.last_name,  ps.first_name, date_format(week_of, '%Y-%m-%d') as week_of, ps.person_id 
    from PAY_STUB ps order by first_name, last_name, week_of
  '''
  )

  return json.dumps(stub_choices)


def get_stub_data(person_id, week_of):  


  stub_data = utils.select('''
    select 
    last_name as LAST_NAME,
    first_name as FIRST_NAME,
    "000-00-0000" as SOCIAL,
    week_of + interval '1' week as PERIOD_END,
    concat(week_of, ' - ', week_of + interval '6' day) as PERIOD_SPAN,
    fed_withholding as FED,
    social_security_tax as SOC,
    medicare_tax as MED,
    nys_withholding as STATE,
    gross_wages as GROSS,
    gross_wages - fed_withholding - social_security_tax - medicare_tax - nys_withholding as NET,
    round(hours_worked * nominal_scale,2) as HOURS,
    pay_rate as RATE
    from PAY_STUB 
    where person_id = {person_id}
    and week_of = "{week_of}"
  '''.format(**locals())
  )

  stub_ytd_data = utils.select('''
    select 
    sum(fed_withholding) as FEDYTD,
    sum(social_security_tax) as SOCYTD,
    sum(medicare_tax) as MEDYTD,
    sum(nys_withholding) as STATEYTD,
    sum(gross_wages) as GYTD,
    sum(gross_wages - fed_withholding - social_security_tax - medicare_tax - nys_withholding) as NETYTD
    from PAY_STUB 
    where person_id = {person_id}
    and year("{week_of}" + interval '1' week) = year(week_of+interval '1' week) 
    and week_of <= date("{week_of}")
  '''.format(**locals())
  )

  # make one dictionary of the two result sets
  result = stub_data[0] # start with stub_data
  result.update(stub_ytd_data[0]) #add the YTD stuff to it

  if utils.hostname() == 'salsrv':
    result["BUSS_INFO_LINE"] = "SALUMI dba Ultraviolet Enterprises 5600 Merrick RD, Massapequa, NY 11758 516-620-0057"
  else:  
    result["BUSS_INFO_LINE"] = "PLANCHA dba Infrared Enterprises 931 Franklin AVE, GardenCity, NY 516-246-9459"
  return result


def fodt_text(stub_data):
  doc = open('/var/www/paystub_template.fodt').read()

  for key, value in stub_data.items():
    doc = re.sub(r'\$'+key+r'\b', str(value), doc)

  return doc


def gen_fodt_and_pdf(stub_data):
  
  doc = fodt_text(stub_data)
  fodtname = "/tmp/paystub.fodt"
  new_fodt = open(fodtname, 'w')
  new_fodt.write(doc)
  new_fodt.close()

  #subprocess.call(['soffice', '--headless', '--convert-to pdf', '--outdir /var/www/winelists/', fodtname])
  os.system('export HOME=/tmp ; soffice --headless --convert-to pdf --outdir /tmp/ ' + fodtname)


def index(req, stub_select): #person_id, week_of):
  
  person_id, week_of = stub_select.split(',')

  stub_data = get_stub_data(person_id, week_of)
  gen_fodt_and_pdf(stub_data)

  if req: req.content_type = 'application/pdf'
  if req: req.content_disposition = 'attachment; filename=foobark'

  pdf = open('/tmp/paystub.pdf').read()
  return pdf



if __name__ == '__main__':
  print gen_fodt_and_pdf()

