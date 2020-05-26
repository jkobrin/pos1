# -*- coding: utf-8 -*-
import json
import MySQLdb
from xml.sax.saxutils import escape
from datetime import date
import os, subprocess

import utils
import config_loader


def clean(data_str):
  NULLITIES = ('None', 'null', 'NULL', 'Null', '')
  if data_str.strip() in NULLITIES: return None
  else: return data_str


def get_wine_xml():  

  winecats = utils.select('''
    select category from sku 
    where active = true and listorder > 0 and bin is not null 
    group by category order by min(listorder)''')

  for num, cat in enumerate(winecats):
    cat = cat['category']

    wine_items = utils.select('''
      select * from sku
      where category = '%(cat)s'
      and listorder > 0
      and active = true
      and bin is not null
      and bin != '0'
      order by listorder
      ''' % locals())

    if (cat in ('Red Wine', 'Bubbly', 'Bottled Beer', 'Beer', 'Sparkling Wine', 'House Cocktails')
        or config_loader.config_dict['new_page_for_white_wine'] and cat == 'White Wine'):
      style = 'P19' #this style starts new page
    else:
      style = 'P20'

    yield '''
   <text:h text:style-name="%s">%s</text:h>
   ''' % (style, escape(cat))

    if cat in ('House Cocktails', 'Beer', 'Classic Cocktails'):	
      yield '''<text:p/>'''


    current_subcategory = None

    for item in wine_items:
      binnum, name, description, subcategory  = (
        clean(escape(unicode(item[key]))) for key in ['bin', 'name', 'description', 'subcategory']
      )
      listprice = item['retail_price']

      # do location heading if location changed
      if current_subcategory != subcategory and subcategory is not None:
        current_subcategory = subcategory
        yield '''<text:p text:style-name="Psubcat"><text:span text:style-name="T1">%s</text:span></text:p>'''%subcategory

      yield '''<text:p text:style-name="P4">%s.<text:tab/>%s<text:s text:c="5"/>%d'''%(binnum, name, listprice)
      if description:
        for line in description.splitlines():
          yield '''<text:line-break/>%s''' % line
      yield '</text:p>'
      yield '''<text:p text:style-name="P18"/>'''
      
      if cat in ('House Cocktails', 'Classic Cocktails', 'Beer'):	
      	yield '''<text:p/>'''


def fodt_text():
  doc = open('/var/www/winelist_head.xml.frag').read()
  for frag in get_wine_xml():
    doc += frag
  if config_loader.config_dict['use_wine_fun']:
    doc += open('/var/www/winefun.xml.frag').read()
  elif utils.hostname() == 'salsrv':
    doc += open('/var/www/wineaward.xml.frag').read()
  doc += open('/var/www/winelist_tail.xml.frag').read()

  return doc

def index(req):
  return  fodt(req)


def gen_fodt_and_pdf(req = None):
  
  doc = fodt_text()
  winelists_dir = "/var/www/winelists/"
  fodtname = winelists_dir + str(date.today())+".fodt"
  new_fodt = open(fodtname, 'w')
  new_fodt.write(doc.encode('utf-8'))
  new_fodt.close()

  #subprocess.call(['soffice', '--headless', '--convert-to pdf', '--outdir /var/www/winelists/', fodtname])
  os.system('soffice "-env:UserInstallation=file:///tmp/LibreOffice_Conversion" --headless --convert-to pdf --outdir ' + winelists_dir + ' ' + fodtname)
  return 'done'


def fodt(req):
  if req:
    req.content_type = 'application/text'
  doc = fodt_text()

  return doc


def index3():
  #sys.stdout.write('Content-type: application/octet-stream')
  sys.stdout.write('Content-type: text/xml')
  sys.stdout.write(open('/var/www/winelist_head.xml.frag').read())
  for frag in get_wine_xml():
    sys.stdout.write(frag)
  sys.stdout.write(open('/var/www/winelist_tail.xml.frag').read())


def index2():
  new_winelist_name = './tmp/winelist.'+str(date.today())+'33.fodt'
  winelist = open(new_winelist_name, 'w')

  winelist.write(open('winelist_head.xml.frag').read())
  for frag in get_wine_xml():
    winelist.write(frag)
  winelist.write(open('winelist_tail.xml.frag').read())

  winelist.close()

  return '<html><body> <a href="'+new_winelist_name+'"></body></html>'


if __name__ == '__main__':
  print gen_fodt_and_pdf()

