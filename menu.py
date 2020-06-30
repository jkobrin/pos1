# -*- coding: utf-8 -*-
import MySQLdb
from xml.sax.saxutils import escape
import datetime
import os, subprocess
import json

import utils
import config_loader
from config import winecats

BTG = 'by the glass'

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
    <script type="text/javascript" src="menufuncs.js?id=%s"></script>
    <body>
  '''%(datetime.datetime.now(), datetime.datetime.now())

  supercats = utils.select('''
    select supercategory from sku 
    where active = true and listorder > 0 and bin is not null 
    and supercategory is not null
    group by supercategory order by min(listorder)''')

  for supercat in supercats:
    supercat = supercat['supercategory']
    yield '''<h1 onclick="majority_toggle_child_checkboxes(this)">%s</h1>
             <div class="supercategory" id="%s">''' % (escape(supercat), supercat)

    cats = utils.select('''
      select category from sku 
      where active = true and listorder > 0 and bin is not null 
      and supercategory = %s
      group by category order by min(listorder)''', args=[supercat])

    for cat in [c['category'] for c in cats]:
      is_wine = winecats.search(cat)
      yield '''<div class="category accordion" id="%s">'''%cat
      yield '''<input type="checkbox" name="%s%s" id="%s%s">'''% (supercat, cat, supercat, cat)
      #yield '''<h2 ><label for="%s%s">%s</label></h2>'''%(supercat, cat, escape(cat))
      yield '''<center><h2><label class="cat_label" for="%s%s">%s</label></h2></center>'''%(supercat, cat, escape(cat))
      yield '''<div class="cat_content content">'''

      items = utils.select('''
          select * from sku
          where category = '%(cat)s'
          and listorder > 0
          and active = true
          and bin is not null
          and bin != '0'
          order by scalable desc, listorder #put btg first
          ''' % locals())


      current_subcategory = None
      for number, item in enumerate(items):
        sku_id, binnum, name, display_name, description, subcategory= (
          clean(escape(unicode(item[key]))) for key in ['id', 'bin', 'name', 'display_name', 'description', 'subcategory']
        )
        display_name = display_name or name #if display_name is blank default to name
        listprice = item['retail_price'] 
        if not is_wine: binnum = ''
        if item['scalable'] and is_wine: subcategory = BTG

        if subcategory is None and current_subcategory is None:
          subcategory = cat

        # do subcat heading if subcat changed
        if current_subcategory != subcategory and subcategory is not None:
          if current_subcategory is not None: yield '''</div>'''
          current_subcategory = subcategory
          yield '''
          <div class="subcategory" id="%s">
          <h3 onclick="majority_toggle_child_checkboxes(this.parentElement)"> &#x2011;&#x2011;%s&#x2011;&#x2011; </h3>
          '''%(current_subcategory.replace(' ', '_'), current_subcategory)

        if description:
          descriptions = description.split('|')
          if len(descriptions) > 1:
            description = descriptions[1]
            pre_text = descriptions[0]
            yield '''<div class="description">%s</div>'''%pre_text
        
        yield '''<div class="item_block accordion">'''
        yield '''<input type="checkbox" name="%s" id="%s">'''% (sku_id, sku_id)
        yield '''<label for="%s">'''%sku_id
        yield '''<div class="binnum">%s</div>'''%binnum
        yield '''<div class="item_name">%s</div>'''%display_name
        yield '''<div class="item_price">'''
        if item['scalable'] and item['qtprice']:
          yield '''%g'''%item['qtprice']
          if listprice > 0:
            description += '<br> Bottle: %g'%listprice
        elif listprice > 0:
          yield '''%g'''%listprice
        yield '''</div>'''
        yield '''</label>'''

        yield '''<div class="description content">'''
        if description:
          for line in description.splitlines():
            yield '''%s<br>''' % line
        else:
            yield '''-no info-'''
          
        yield '</div>' #description

        yield '</div> <!-- item block -->' #item_block

      if current_subcategory is not None: yield '''</div>''' #subcategory

      yield '''</div></div> <!-- cat_content and cat -->'''#cat_content and cat

    yield '''</div>''' #supercat

  yield "</body></html>"


def index(req):
  return "\n".join(get_menu_html())
    
  
def generate_and_post():
  # get all lines from generator before touching file, so if
  # there is an error we don't overwrite old file.
  menu = list(get_menu_html())

  outfile = open("/var/www/salumiweb/menu.html", "w")
  outfile.writelines(menu)
  outfile.close()

  return json.dumps(None)
    


if __name__ == '__main__':
  print gen_fodt_and_pdf()

