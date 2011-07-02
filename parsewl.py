#! /usr/bin/python
import yaml
import sys

wl = yaml.load(open(sys.argv[1]))
wl_out = sys.stdout

orderview = len(sys.argv) > 2 and sys.argv[2] == 'order'

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
    listprice = wine.get('listprice') or ''
    qtprice = wine.get('qtprice') or ''
    if not qtprice:
      sys.stderr.write('no qt price for bin %s\n'%binnum)
    if not listprice:
      if qtprice:
        listprice = '|' + str(wine['qtprice'])
      else:
        raise Exception('no list or qt price for bin %s' %binnum)
    byline = wine.get('byline')

    if orderview:
      prnt('%s %s %s %s #%s' %(wine.get('catalog'), wine['name'], byline, wine['frontprice'], binnum))
      continue
      
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
