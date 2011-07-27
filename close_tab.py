fileencoding = "iso-8859-1"


import json
import MySQLdb
import cups
import tempfile, os
import texttab

SPRINT_OPTIONS = {
 'page-border':'double', 'page-left':'48', 'page-top':'36',
}

PRINT_OPTIONS = {
 'page-border':'single', 
 'page-left':'12',
  'media':'Custom.3.125x%(page_length)sin',
 'lpi': '4'
}

PRINTER_NAME = 'CITIZEN-CT-S310'

LINES_PER_INCH = 4
CHARACTERS_PER_INCH = 10 # CUPS default
PAGE_WIDTH_IN_INCHES = 3.125
PAGE_WIDTH_IN_CHARS = PAGE_WIDTH_IN_INCHES * CHARACTERS_PER_INCH - 5

def index(req, table, shouldPrint, serverpin, close=True):


  conn = MySQLdb.connect (host = "localhost",
                        user = "pos",
                        passwd = "pos",
                        db = "pos")

  cursor = conn.cursor()

  shouldPrint = (shouldPrint == 'true')

  if shouldPrint:
    receipt_text = texttab.get_tab_text(table, serverpin, cursor)

    # Figure out how long the receipt should be
    receipt_lines = receipt_text.split('\n')
    print receipt_lines
    num_lines_of_text = len(receipt_lines);
    num_wrapping_lines = \
      len([line for line in receipt_lines if len(line) > PAGE_WIDTH_IN_CHARS])
    # I assume no line wraps more than once  
    print 'num_wrapping_lines', num_wrapping_lines
    num_lines_of_text += num_wrapping_lines
    print 'num_lines_of_text', num_lines_of_text
    page_length_in_inches =  num_lines_of_text / float(LINES_PER_INCH) + 1
    page_length_in_inches = min(page_length_in_inches, 11) 

  if close:
    cursor.execute('''
      UPDATE order_group
      SET is_open = FALSE, closedby = %(serverpin)s, updated = now()
      WHERE is_open = TRUE
      AND table_id = "%(table)s"
    ''' % locals())

  cursor.close()
  conn.close()

  if shouldPrint:
    recfile = tempfile.NamedTemporaryFile(delete=False)
    #recfile = open('/tmp/recfile9', 'w')
    recfile.write(receipt_text)
    filename = recfile.name
    recfile.close()

    conn = cups.Connection()
    #conn.getDefault()

    
    page_length_in_inches
    PRINT_OPTIONS['media'] = PRINT_OPTIONS['media'] % \
      {'page_length': page_length_in_inches}

    print PRINT_OPTIONS
    conn.printFile(PRINTER_NAME, filename, 'receipt', PRINT_OPTIONS)
    os.remove(filename)

  return json.dumps(None)

if __name__ == '__main__':
  print index(None, '1', 'true', 1, close=False)
