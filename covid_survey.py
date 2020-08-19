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
      return '''
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <html>
    <body style="background: yellow">
    <H1> WARNING! YOU ARE A POTENTIAL COVID HAZARD!</H1>
    <H2> Your responses have been recorded. Please leave work <i>immediately</i> and call or text your manager. Thank you.</H2>
    </body>
    </html>
    '''

  return '''
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <html>
    <body>
    Thank you. Your responses have been recorded. It is safe for you to begin work.
    <p>
    <center><button id=done onclick='window.close()'>OK</button></center>
    </body>
    </html>
    '''

if __name__ == '__main__':
  print datetime.now().strftime("%Y_%m_%d")
