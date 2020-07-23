import Image, ImageFont, ImageDraw
import base64
from io import BytesIO
from os import path

LINE_HEIGHT = 300
LEFT_INNER_BORDER = 100
RESOURCE_DIR = '/var/www/resources'
CERTIFICATE_IMAGE_FILENAME = 'SalumiPlanchaGiftCertificate.png'


class GiftCert(object):
  
  def __init__(self, item):
    self.item = item
    if self.is_gift():
      self.serial = str(self.item['id'])
      self.value = str(int(self.item['price']))


  def is_gift(self):
    return self.item['name'].startswith('gift')


  def get_cert_image_data(self):
    serial = self.serial
    amt_text = '%s'%self.value
    pre_text = '$ '
    post_text = ' $'

    image = Image.open(path.join(RESOURCE_DIR, CERTIFICATE_IMAGE_FILENAME))
    # initialise the drawing context with
    # the image object as background
    draw = ImageDraw.Draw(image)

    # create font object with the font file and specify
    # desired size
    amt_text_font = ImageFont.truetype('DejaVuSans.ttf', size=140)
    pre_text_font = ImageFont.truetype('DejaVuSans.ttf', size=50)
    post_text_font = ImageFont.truetype('DejaVuSans.ttf', size=50)
    codefont = ImageFont.truetype('IDAutomationHC39M Free Version.ttf', size=24, encoding='symb')
    #codefont = ImageFont.truetype('FreeSerif.ttf', size=50)
    color = 'rgb(0, 0, 0)' # black
     
    # figure out where to position the amount text
    width, height = image.size
    amt_text_w, amt_text_h = draw.textsize(amt_text, font=amt_text_font)
    pre_text_w, pre_text_h = draw.textsize(pre_text, font=pre_text_font)
    post_text_w, post_text_h = draw.textsize(post_text, font=post_text_font)
    amt_text_position = ( (width - amt_text_w)/2, LINE_HEIGHT - amt_text_h) #centered
    amt_text_position_x, amt_text_position_y = amt_text_position
    pre_text_position = (amt_text_position_x - pre_text_w, LINE_HEIGHT - amt_text_h/2 - pre_text_h/2)
    post_text_position = (amt_text_position_x + amt_text_w, LINE_HEIGHT - amt_text_h/2 - post_text_h/2)

    #draw amount over the background image at amt_position
    draw.text(pre_text_position, pre_text, fill=color, font=pre_text_font)
    draw.text(amt_text_position, amt_text, fill=color, font=amt_text_font)
    draw.text(post_text_position, post_text, fill=color, font=post_text_font)

    draw.text((LEFT_INNER_BORDER, LINE_HEIGHT + 20), '*%s*'%serial, fill=color, font=codefont)

    image = image.transpose(Image.ROTATE_90)

    # return the finished image by saving to a bystring and
    # returning it as a data url
    with BytesIO() as f:
      image.save(f, format='PNG')
      return f.getvalue()

  def get_image_data(self):

    if self.is_gift():
      image_data = self.get_cert_image_data()
    else:
      with open(path.join(RESOURCE_DIR, '%s.png'%self.item['filename'])) as f:
        image_data = f.read()

    return image_data
    

  def get_data_url(self):
    return 'data:image/png;base64,{}'.format(base64.b64encode(self.get_image_data()))


if __name__ == '__main__':
  gc = GiftCert(123456, 180)
  gc.print_out()
    
