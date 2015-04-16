
import utils



def index(req):

  colnames, records = utils.select('''
	SELECT * from monthly_withholding
  ''',
  incursor=None,
    label='separate'
  )


  html = (
    '''  
      <html>
      <body>
  ''' )
  html += (
    utils.tohtml(
      'Wages and withholding by month',
      colnames,
      records,
      breakonfirst = True
    ) +
    '''</body></html>'''
    )

  return html
