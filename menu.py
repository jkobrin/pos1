# -*- coding: utf-8 -*-
import MySQLdb
from xml.sax.saxutils import escape
import datetime
import os, subprocess
import json

import utils
import config

ONLINE = False
BTG = 'by_the_glass'

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

  cfg = config.load_config()
  for supercat in (sc for sc in cfg['menu']['supercategories'] if sc['name'] != 'tables' and sc['listorder'] > 0):

    yield '''<h1 onclick="majority_toggle_child_checkboxes(this)">%s</h1>
             <div class="supercategory" id="%s">''' % (escape(supercat['name']), supercat['name'])

    for cat in (cat for cat in supercat['categories'] if cat['listorder'] > 0):
      is_wine = config.winecats.search(cat['name'])
      yield '''<div class="category accordion" id="%s">'''%cat['name']
      yield '''<input type="checkbox" name="%s%s" id="%s%s">'''% (supercat['name'], cat['name'], supercat['name'], cat['name'])
      #yield '''<h2 ><label for="%s%s">%s</label></h2>'''%(supercat, cat, escape(cat))
      yield '''<center><h2><label class="cat_label" for="%s%s">%s</label></h2></center>'''%(supercat['name'], cat['name'], escape(cat['name']))
      yield '''<div class="cat_content content">'''

      current_subcategory = None
      for item in (item for item in cat['items'] if item['listorder'] > 0):

        sku_id, binnum, name, display_name, description, subcategory= (
          clean(escape(unicode(item[key]))) for key in ['id', 'bin', 'name', 'display_name', 'description', 'subcategory']
        )
        if cat['name'] != config.BTG_NAME and item.get('is_glass'):
          continue

        display_name = display_name or name #if display_name is blank default to name
        listprice = item['retail_price'] 
        if not is_wine: binnum = ''

        if subcategory is None and current_subcategory is None:
          subcategory = cat['name']

        # do subcat heading if subcat changed
        if current_subcategory != subcategory and subcategory is not None:
          if current_subcategory is not None: yield '''</div>'''
          current_subcategory = subcategory
          yield '''
          <div class="subcategory" id="%s">
          <h3 onclick="majority_toggle_child_checkboxes(this.parentElement)"> &#x2011;&#x2011;%s&#x2011;&#x2011; </h3>
          '''%(current_subcategory.replace(' ', '_'), current_subcategory)


        if item.get('pre_text'):
            yield '''<div class="description">%s</div>'''%item['pre_text']
        
        yield '''<div class="item_block accordion">'''
        yield '''<input class="collapser" type="checkbox" name="%s_%s" id="%s_%s">'''% (subcategory, sku_id, subcategory, sku_id)
        yield '''<label for="%s_%s">'''%(subcategory, sku_id)
        yield '''<div class="binnum">%s</div>'''%binnum
        yield '''<div class="item_name">%s</div>'''%display_name
        yield '''<div class="item_price">'''
        if item.get('is_glass'):
          yield '''%g'''%item['qtprice']
          if item.get('bottle_price') > 0:
            description += '<br> Bottle: %g'%item['bottle_price']
        elif item['retail_price'] > 0:
          yield '''%g'''%item['retail_price']
          if item['qtprice']and item['scalable']> 0:
            description += '<br> Glass: %g'%item['qtprice']
        yield '''</div>'''
        yield '''</label>'''

        yield '''<div class="description content">'''
        if description:
          for line in description.splitlines():
            yield '''%s<br>''' % line
        else:
            yield '''-no info-'''
        if item.get('picture'):
            yield '''<img style="float: right" height="200px" width="200px" src="%s"/>'''%item['picture']
        if ONLINE:
            yield 'Add to cart: <input type="checkbox" name="order" id="ord">'
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

