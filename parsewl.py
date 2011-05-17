#! /usr/bin/python
import yaml
import sys

wl = yaml.load(open(sys.argv[1]))
wl_out = sys.stdout

quartino_only = len(sys.argv) > 2 and sys.argv[2] == 'quartino-only'

def prnt(strng = ''):
  strng = strng.encode('utf-8')
  wl_out.write(strng)
  wl_out.write('\n')

for category in wl:
  prnt(category['name'])
  prnt()
  for wine in category['items']:
    binnum = wine.get('bin')
    if not binnum: continue
    numtabs = 1 #5 - len(name)/8
    frontprice = wine['frontprice']
    #frontprice = wine.get('frontprice', 0) or 0
    listprice = wine.get('listprice') or ''
    #  continue  
    #listprice = wine.get('listprice', str(int(frontprice * 1.5 + 10)) + '?')
    #if wine.get('qt'):
    #  listprice = str(wine['qtprice']) + ' | ' + str(listprice)
      #listprice = ' )--|  ' + str(wine['qtprice']) + '|' + str(listprice)
    if not listprice:
      listprice = '|' + str(wine['qtprice'])
    byline = wine.get('byline')
    if quartino_only:
      listprice = str(wine.get('qtprice'), 'no')

    prnt('%s.\t%s      %s'%(binnum, wine['name'], listprice))
    if byline:
      prnt('\t' + byline)
    grape = wine.get('grape') or wine.get('grapes')
    if grape:
      prnt('\tGrape: ' + grape)
    notes = wine.get('notes')
    if notes:
      prnt('\t' + notes)
    prnt()
