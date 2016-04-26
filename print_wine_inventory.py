fileencoding = "iso-8859-1"

import json
import tempfile, os, sys
import queries, utils
import subprocess

TEXTWIDTH = 25

def index(req = None):
    winelist = utils.select('''
      select category, bin as binnum, name, round(estimated_units_remaining,2) est_count 
      from winelist_inv_pure where bin !=0 and category != 'House Cocktails' order by category, bin;
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
		
if __name__ == '__main__':
    index()
