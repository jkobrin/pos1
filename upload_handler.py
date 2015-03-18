from mod_python import util


def menu(req, **menus):

  response = ''

  for name, filedata in menus.items():
    if filedata:
      menu_file = open('/var/www/salumiweb/menus/%s.pdf'%name, 'w')
      menu_file.write(filedata.value)
      menu_file.close()
      response += '%s menu uploaded\n'%name
    
  return response or 'no files uploaded'
