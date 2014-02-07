fileencoding = "iso-8859-1"


import json
import tempfile, os
import queries
import subprocess

TEXTWIDTH = 25

def go():
    weekly_pay = queries.weekly_pay(printmode = 1)

    for rec in weekly_pay:
	slip_text = get_slip_text(rec)
    	slipfile = tempfile.NamedTemporaryFile(delete=False)
    	slipfile.write(slip_text)
    	filename = slipfile.name
    	slipfile.close()
    	subprocess.call(['enscript', '--font=Courier-Bold@11/16', '-B', '-MEnv10', filename])
    	os.remove(filename)
		

def get_slip_text(rec):
    
    text = ('%s %s'%(rec['first_name'], rec['last_name'])).center(TEXTWIDTH) +'\n'
    for k,v in rec.items():
        text += "%s: %s\n"%(k,v)

    return text
    
    
if __name__ == '__main__':
    go()
