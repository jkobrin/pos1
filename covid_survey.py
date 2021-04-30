from datetime import datetime

def index(req, **formdata):

  formdata['date'] = datetime.now().strftime("%Y_%m_%d")

  survey_file = open('/var/www/covid_surveys/%(fname)s_%(lname)s_%(date)s'%formdata, 'w')
  survey_file.write('''
    Name: {fname} {lname}
    Date: {date}

    Question 1: {q1}
    Question 2: {q2}
    Question 3: {q3}
    Question 4: {q4}
   '''.format(**formdata))

  survey_file.close()
    
  for key, val in formdata.items():
    if key in ('q1', 'q2', 'q3', 'q4') and val == 'yes':
      pass
      '''
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <html>
    <body style="background: yellow">
    <H1> Practice Social Distancing</H1>
    <H2> Thank you.</H2>
    </body>
    </html>
    '''

  return '''
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <html>
    <body>
    Thank you. Your responses have been recorded.
    <p>
    <center><button id=done onclick='window.close()'>OK</button></center>
    </body>
    </html>
    '''

if __name__ == '__main__':
  print datetime.now().strftime("%Y_%m_%d")
