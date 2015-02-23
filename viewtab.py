
import json
import MySQLdb
import utils


def index(req, name):

  colnames, results = utils.select('''
    SELECT * from %(name)s
  ''' % locals(),
    incursor=None,
    label='separate'
  )
  
  html = (
    '''  
      <html>
      <body>
    ''' + 
    utils.tohtml(
      name, 
      colnames,
      results
    ) +
    '''</body></html>'''

  )

  return html

if __name__ == '__main__':
  print index(None)
