fileencoding = "iso-8859-1"

import json
import tempfile, os, sys
import queries, utils
import subprocess
from mylog import my_logger

TEXTWIDTH = 27

def index(req = None):
    my_logger.info('inventory')
    winelist = utils.select('''
      select category, bin as binnum, name, round(estimated_units_remaining,2) est_count 
      from winelist_inv where bin !=0 and category != 'House Cocktails' order by category, bin;
    '''
    , label=True)

    outfile = tempfile.NamedTemporaryFile(delete=False)
    filename = outfile.name
    catname = None;
    for rec in winelist:
      if catname != rec['category']:
        catname = rec['category']
        outfile.write(catname+':\n')

      outfile.write(
        str(rec['binnum']).ljust(5) + 
        rec['name'][:10].encode('latin1', 'replace') + ' ' + 
        str(rec['est_count']) + '\n'
      )

    outfile.close()
    subprocess.call(['enscript', '--font=Courier-Bold@11/16', '-B', '-MEnv10', filename])
    os.remove(filename)
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
