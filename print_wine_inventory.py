fileencoding = "iso-8859-1"

import json
import tempfile, os, sys
import queries, utils
import subprocess
from mylog import my_logger

import inventory

TEXTWIDTH = 27

def go(query):
    my_logger.info('inventory')
    queryfunction = getattr(inventory, 'get_'+query)
    winelist = queryfunction(None)
    winelist = json.loads(winelist) #convert from json format to python native
    # winelist = utils.select('''
    #  select category, bin as binnum, name, round(estimated_units_remaining,2) est_count 
    #  from sku_inv where bin !=0 and category != 'House Cocktails' order by category, bin;
    #'''
    #, label=True)

    inventory_text = '';
    catname = None;
    for rec in winelist:
      # check if we are in a new category
      if catname != rec['category']:
          # if we just finished a previous category, insert a
          # page-break
        if catname is not None:
          inventory_text += ''
        # and in any case print the new category name
        catname = rec['category']
        inventory_text += catname+':\n'


      inventory_text += (
        ('%s'%rec.get('bin')).ljust(5) + 
        rec.get('name')[:10] + ' ' + 
        str(rec['estimated_units_remaining']) + '\n'
      )

    utils.print_slip(inventory_text )#, outfile = '/var/www/paystubs/wi')
    return  json.dumps(None)
		

def cellar_list(req = None):
    my_logger.info('cellar list')
    cellarlist = utils.select('''
      select bin as binnum, name, round(estimated_units_remaining) est_count, byline, listprice
      from winelist_inv where bin !=0 and cellar_listorder != 0 and cellar_listorder is not null
      order by cellar_listorder;
    '''
    , label=True)

    outfile = tempfile.NamedTemporaryFile(delete=False)
    filename = outfile.name
    for rec in cellarlist:
      outfile.write(
        rec['name'][:TEXTWIDTH].encode('latin1', 'replace') + '\n' + 
        'bin '+str(rec['binnum']) + ', ' +
        str(int(rec['est_count'])) + ' bottles' + ',  $' + str(rec['listprice']) + '\n\n'
      )

    outfile.close()
    subprocess.call(['enscript', '--font=Courier-Bold@11/16', '-B', '-MReceiptRoll', filename])
    #subprocess.call(['cat', filename])
    os.remove(filename)
    return  json.dumps(None)
		
if __name__ == '__main__':
    #index()
    cellar_list()
