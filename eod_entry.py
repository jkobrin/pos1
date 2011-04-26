import queries
import texttab

take_name, take_cash, take_credit, take_credit_tips, exit = xrange(5)
state =  take_name

info_by_server =  queries.nightly_sales_by_server(label=True)
current_server_info = None

server_info = {}

class server_inf(object):
    
  def __init__(self, kv):
    self.server = server
    self.sales = sales * (1 + texttab.TAXRATE)
    self.credit = None
    self.credit_tips = None
    self.cash = None

  def cash_tips(self):
    if self.credit is not None and self.cash is not None:
      return  self.credit + self.cash - self.sales
      
  def all_tips(self):
    if self.credit_tips is not None and self.cash_tips() is not None:
      return self.credit_tips() + self.cash_tips()
      
  def format(self):
    return '%s --  cash:%s   credit:%s   sales:%s   credit tips:%s    cash tips:%s   all tips:%s' % (
      self.server, self.cash, self.credit, self.sales, self.credit_tips, self.cash_tips(), self.all_tips()
    )  

#for row in info_by_server:
  #server_info = {row[

def prompt():
  global state, current_server_info

  return {
    take_name: "Server last name",
    take_cash: "Cash collected (including cash tips)",
    take_credit: "Credit sales",
    take_credit_tips: "Credit tips",
    exit: "Programming error",
    }[state] + ": "


def find(pred):
  for row in info_by_server:
    if pred(row):
      return row

def addto(category, num):
    try: num = float(num)
    except: return 'not a number'
    current_server_info[category] = \
      (current_server_info[category] or 0) + num
    return current_server_info[category]  

def gostate(newstate):
  global state

  state = newstate
  return format_current_server_info()

def respond(said):
  global state, current_server_info

  resp = ''

  if state == take_name:
    if not said: state = exit
    else:
      current_server_info = find(lambda inf: inf['server'] == said)
      if current_server_info:
        resp = gostate(take_cash)
      else: resp = 'no such server had sales tonight'
  elif state == take_cash:
    if not said: resp = gostate(take_credit)
    else: resp = addto('cash', said)
  elif state == take_credit:
    if not said: resp = gostate(take_credit_tips)
    else: resp = addto('credit', said)
  elif state == take_credit_tips:
    if not said: 
      resp = gostate(take_name)
    else: resp = addto('credit_tips', said)
  else:
    resp = 'Programming error: Unknown state: %s' % state

  return resp

for row in info_by_server:
  current_server_info = row
  print format_current_server_info()

while state != exit:
  said = raw_input(prompt())
  print respond(said)

for row in info_by_server:
  row['cash_tips'] = row['credit'] + row['cash'] - row['sales']
  row['total_tips'] = row['cash_tips'] + row['credit_tips']

grand_total_tips = sum(row['total_tips'] for row in info_by_server)

print info_by_server  

print 'all tips: %s' % grand_total_tips




