
import json
import MySQLdb
import cups
import tempfile, os
import texttab

print_options = {
 'page-border':'double', 'page-left':'48', 'page-top':'36', 'media':'Custom.4.25x11in'
}

def index(req, table, shouldPrint, serverpin):

  shouldPrint = (shouldPrint == 'true')

  if shouldPrint:
    receipt_text = texttab.get_tab_text(table)


  conn = MySQLdb.connect (host = "localhost",
                        user = "pos",
                        passwd = "pos",
                        db = "pos")

  cursor = conn.cursor()

  cursor.execute('''
    UPDATE order_group
    SET is_open = FALSE, closedby = %(serverpin)s
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
    conn.printFile(conn.getDefault(), filename, 'receipt', print_options)
    os.remove(filename)

  return json.dumps(None)

if __name__ == '__main__':
  print index(None, 'B12', 'true')
