# -*- coding: utf-8 -*-
import MySQLdb
from xml.sax.saxutils import escape
import datetime
import os, subprocess

import utils
import config_loader


def clean(data_str):
  NULLITIES = ('None', 'null', 'NULL', 'Null', '')
  if data_str.strip() in NULLITIES: return None
  else: return data_str


def get_menu_html():  

  yield '''
<html>
    <head>
      <meta charset = "UTF-8">
      <title>MENU</title>
      <link rel = "stylesheet" type = "text/css" href = "menustyle.css?id=%s" />
    </head>
  <body>
  '''%datetime.datetime.now()
  supercats = utils.select('''
    select supercategory from sku 
    where active = true and listorder > 0 and bin is not null 
    group by supercategory order by min(listorder)''')

  for supercat in supercats:
    supercat = supercat['supercategory']
    yield '''<h1>%s</h1> <div class="supercategory" id="%s">''' % (escape(supercat), supercat)

    cats = utils.select('''
      select category from sku 
      where active = true and listorder > 0 and bin is not null 
      and supercategory = %s
      group by category order by min(listorder)''', args=[supercat])

    for cat in cats:
      cat = cat['category']
      yield '''<div class="category accordion">'''
      yield '''<input type="checkbox" name="%s%s" id="%s%s">'''% (supercat, cat, supercat, cat)
      yield '''<h2 ><label for="%s%s">%s</label></h2>'''%(supercat, cat, escape(cat))
      yield '''<div class="cat_content content">'''

      items = utils.select('''
        select * from sku
        where category = '%(cat)s'
        and listorder > 0
        and active = true
        and bin is not null
        and bin != '0'
        order by listorder
        ''' % locals())


      current_subcategory = None
      for item in items:
        utils.expand_extra_fields(item)
        sku_id, binnum, name, display_name, description, subcategory= (
          clean(escape(unicode(item[key]))) for key in ['id', 'bin', 'name', 'display_name', 'description', 'subcategory']
        )
        display_name = display_name or name #if display_name is blank default to name
        listprice = item['retail_price']

        # do subcat heading if subcat changed
        if current_subcategory != subcategory and subcategory is not None:
          current_subcategory = subcategory
          yield '''<h3>%s</h3>'''%(current_subcategory)
        if description:
          descriptions = description.split('|')
          if len(descriptions) > 1:
            description = descriptions[1]
            pre_text = descriptions[0]
            yield '''<div class="description">%s</div>'''%pre_text
        
        yield '''<div class="item_block accordion">'''
        yield '''<input type="checkbox" name="%s" id="%s">'''% (sku_id, sku_id)
        yield '''<div class="binnum">%s</div>'''%binnum
        yield '''<label for="%s">'''%sku_id
        yield '''<div class="item_name">%s</div>'''%display_name
        yield '''</label>'''
        yield '''<div class="item_price">%d</div>'''%listprice

        yield '''<div class="description content">'''
        if description:
          for line in description.splitlines():
            yield '''%s<br>''' % line
        else:
            yield '''-no info-'''
          
        yield '</div>' #description

        yield '</div> <!-- item block -->' #item_block

      yield '''</div></div> <!-- cat_content and cat -->'''#cat_content and cat

    yield '''</div>''' #supercat

  yield "</body></html>"


def index(req):
  global table_of_contents
  table_of_contents= []
  body = "\n".join(get_menu_html())
  toc_html=''
  for head in table_of_contents:
    toc_html += '''<p><a href="#%s">%s</a>'''%(head, head)

  return toc_html + body
    
  

if __name__ == '__main__':
  print gen_fodt_and_pdf()

