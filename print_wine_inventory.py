fileencoding = "iso-8859-1"

import tempfile, os, sys
import queries, utils
import subprocess

TEXTWIDTH = 25

def index(req = None):
    winelist = utils.select('''
      select name, round(estimated_units_remaining) est_count 
      from winelist_inv_pure where bin !=0 order by category, bin;
    '''
    , label=True)

    outfile = tempfile.NamedTemporaryFile(delete=False)
    filename = outfile.name
    for rec in winelist:
      outfile.write(str(rec['est_count']).ljust(4) + rec['name'][:15] + '\n')

    outfile.close()
    subprocess.call(['enscript', '--font=Courier-Bold@11/16', '-B', '-MEnv10', filename])
    os.remove(filename)
    return '<html><body>Wine inventory sent to printer.</body></html>'
		
if __name__ == '__main__':
    index()
