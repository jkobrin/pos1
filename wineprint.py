
import json
import MySQLdb
from xml.sax.saxutils import escape
from datetime import date
import sys

import utils



def get_wine_xml():  

  winecats = utils.select('''select distinct category from active_wine''')
  for cat in winecats:
    cat = cat['category']

    wine_items = utils.select('''
      select * from active_wine
      where category = '%(cat)s'
      and listorder > 0
      order by listorder
      ''' % locals())

    yield '''
   <text:h text:style-name="P19">%s</text:h>
   ''' % escape(cat)

    for item in wine_items:
      binnum, name, listprice, byline, grapes, notes  = (
        escape(str(item[key])) for key in ['bin', 'name', 'listprice', 'byline', 'grapes', 'notes']
      )

      yield '''<text:p text:style-name="P4">%s.<text:tab/>%s<text:s text:c="5"/>%s'''%(binnum, name, listprice)

      nullities = ('None', 'null', 'NULL', 'Null', '')
      if byline not in nullities:
        yield '''<text:line-break/>%s''' % byline
      if grapes not in nullities:
        yield '''<text:line-break/>Grapes: %s''' % grapes
      if notes not in nullities:
        yield '''<text:line-break/>%s''' % notes
      yield '</text:p>'
      yield '''<text:p text:style-name="P18"/>'''


def index(req):
  req.content_type = 'application/text'
  doc = open('/var/www/winelist_head.xml.frag').read()
  for frag in get_wine_xml():
    doc += frag
  doc += open('/var/www/winelist_tail.xml.frag').read()

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
  print index()

