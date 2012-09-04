import queries
import texttab
import sys

take_name, take_cash, take_credit, take_credit_tips, exit = xrange(5)
state =  take_name

lag_hours = (len(sys.argv) > 1 and sys.argv[1]) or 16
info_by_server =  queries.nightly_sales_by_server(label=True, lag_hours=lag_hours)

current_server_info = None

server_info = {}

class server_inf(object):
    
  def __init__(self, server, ccid, sales, taxable_sales, **kv):
    taxable_sales = taxable_sales or 0
    self.server = server
    self.presales = taxable_sales
    self.sales = sales + taxable_sales * texttab.TAXRATE
    self.credit = 0
    self.credit_tips = 0
    self.cash = None
    self.ccid = str(ccid)

  def cash_tips(self):
    if self.credit is not None and self.cash is not None:
      return  self.credit + self.cash - self.sales
      
  def all_tips(self):
    if self.credit_tips is not None and self.cash_tips() is not None:
      return self.credit_tips + self.cash_tips()
      
  def tip_pct(self):
     if self.all_tips() is not None:
       if self.presales:
        return self.all_tips() * 100/ self.presales
       else: return None

  def format(self):
    return '%s %s --  cash:%s   credit:%s   sales:%s   credit tips:%s   cash tips:%s   all tips:%s  tip%%: %s' % (
      self.server, self.ccid, self.cash, self.credit, self.sales, self.credit_tips, self.cash_tips(), self.all_tips(), self.tip_pct()
    )  

for row in info_by_server:
  server_info[row['server'].lower()] =  server_inf(**row)


def prompt():
  global state, server_info

  return {
    take_name: "Server last name",
    take_cash: "collected", #"Cash collected (including cash tips)",
    take_credit: "Credit sales",
    take_credit_tips: "Credit tips",
    exit: "Programming error",
    }[state] + ": "


def get_server_info(name):
    name = name.lower()
    results = [sname for sname in server_info if sname.startswith(name) or server_info[sname].ccid == name]
    if len(results) == 1:
      return server_info.get(results[0]), None
    elif len(results) > 1:
      return None, str(results) + '?'
    else:
      return None, 'no matching server with sales'


def addto(category, num):
    try: num = float(num)
    except: return 'not a number'
    current_server_info.__dict__[category] = \
      (current_server_info.__dict__.get(category) or 0) + num
    return current_server_info.__dict__[category]

def gostate(newstate):
  global state

  state = newstate
  return current_server_info.format()

def respond(said):
  global state, current_server_info

  resp = ''

  if state == take_name:
    if not said: 
      for inf in server_info.values():
        print inf.format() 
      if all(inf.all_tips() for inf in server_info.values()):
        grand_total_tips = sum(inf.all_tips() for inf in server_info.values())
        print 'all tips: %s' % grand_total_tips
    else:
      current_server_info, resp = get_server_info(said)
      if current_server_info:
        resp = gostate(take_cash)
  elif state == take_cash:
    if not said: resp = gostate(take_name)
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

for k,v  in server_info.items():
  current_server_info = v
  print current_server_info.format()

while state != exit:
  said = raw_input(prompt())
  print respond(said.lower())

#for row in info_by_server:
#  row['cash_tips'] = row['credit'] + row['cash'] - row['sales']
#  row['total_tips'] = row['cash_tips'] + row['credit_tips']

grand_total_tips = sum(inf.all_tips() for inf in server_info.values())

for inf in server_info.values():
  print inf.format() 

print 'all tips: %s' % grand_total_tips




