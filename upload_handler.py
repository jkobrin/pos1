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

def resource(req, **resource_files):

  response = ''

  for name, filedata in resource_files.items():
    if filedata:
      resource_file = open('/var/www/resources/%s.pdf'%name, 'w')
      resource_file.write(filedata.value)
      resource_file.close()
      response += '%s resource uploaded\n'%name
    
  return response or 'no files uploaded'
