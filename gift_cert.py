import subprocess, os
from base64 import b16encode

class GiftCert(object):
  
  def __init__(self, item):
    self.item = item

  def is_gift(self):
    return self.item['name'].startswith('gift')

  def is_coupon(self):
    return self.item['name'].startswith('coupon')

  def print_out(self):

    if self.is_gift():
      serial = str(self.item['id'])
      value = str(int(self.item['price']))
      denom = value.ljust(3)
      rjust_denom = value.rjust(3)

      args = [b16encode(arg) for arg in (serial, denom, rjust_denom)] + [serial]

      olddir = os.getcwd()
      thisdir = os.path.dirname(__file__) 
      try:
        if thisdir: os.chdir(thisdir)
        scriptfile = './print_gift_cert.sh'
        subprocess.check_call([scriptfile] + args)
      finally:
        os.chdir(olddir)

    elif self.is_coupon():
      args = ['lp', '/var/www/resources/%s'%self.item['name']]
      subprocess.call(args)


if __name__ == '__main__':
  gc = GiftCert(123456, 180)
  gc.print_out()
    
