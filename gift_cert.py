import subprocess, os
from base64 import b16encode

class GiftCert(object):
  
  def __init__(self, serial, value):
    self.serial = str(serial)
    self.value = str(int(value))

  def print_out(self):

    serial = str(self.serial)
    denom = self.value.ljust(3)
    rjust_denom = self.value.rjust(3)

    args = [b16encode(arg) for arg in (serial, denom, rjust_denom)]

    olddir = os.getcwd()
    thisdir = os.path.dirname(__file__) 
    try:
      if thisdir: os.chdir(thisdir)
      scriptfile = './print_gift_cert.sh'
      subprocess.check_call([scriptfile] + args)
    finally:
      os.chdir(olddir)


if __name__ == '__main__':
  gc = GiftCert(123456, 180)
  gc.print_out()
    
