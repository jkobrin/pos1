import json
import utils
import tempfile, os
import texttab

import subprocess


#SPRINT_OPTIONS = {
# 'page-border':'double', 'page-left':'48', 'page-top':'36',
#}

#PRINT_OPTIONS = {
# 'page-border':'single', 
# 'page-left':'12',
#  'media':'Custom.3.125x%(page_length)sin',
# 'lpi': '4',
  #'penwidth': '3000', #no effect
#}

#PRINTER_NAME = 'CITIZEN-CT-S310'

#LINES_PER_INCH = 4
#CHARACTERS_PER_INCH = 10 # CUPS default
#PAGE_WIDTH_IN_INCHES = 3.125
#PAGE_WIDTH_IN_CHARS = PAGE_WIDTH_IN_INCHES * CHARACTERS_PER_INCH - 5

def index(req, table, shouldPrint, serverpin, close=True):

  cursor = utils.get_cursor()

  shouldPrint = (shouldPrint == 'true')

  receipt_text, gift_certs = texttab.get_tab_text(table, serverpin, cursor)

  if close:
    cursor.execute('''
      UPDATE order_group
      SET is_open = FALSE, closedby = %(serverpin)s, updated = now()
      WHERE is_open = TRUE
      AND table_id = "%(table)s"
    ''' % locals())

  cursor.close()

  if shouldPrint:
    recfile = tempfile.NamedTemporaryFile(delete=False)
    recfile.write(receipt_text.encode('latin1', 'replace'))
    filename = recfile.name
    recfile.close()

    subprocess.call(['enscript', '--font=Courier-Bold@11/16', '-B', '-MEnv10', filename])
    os.remove(filename)

  for cert in gift_certs:
    cert.print_out()

  return json.dumps(None)

if __name__ == '__main__':
  print index(None, 'O1', 'true', 1, close=False)
