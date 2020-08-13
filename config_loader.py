import inspect
import yaml
import os

def passed_options():
  # mod_python for Apache does not put SetEnv directives from apache config into
  # os.environ. This would allow you to know which virtual host, for example, had
  # invoked the code. But they don't pass it in, probably because it can't really
  # be done in a thread-safe way. What they do have is PythonOption which you can
  # set in VirtualHost sections of apache config files and then get from the
  # request object. It is not a global (again, probably cause this cannot be
  # thread-safe) so normally you'd have to pass the request object all down the
  # stack so various functions you call could get the options and know what
  # environment they were operating in. To avoid all the messy parameter
  # passing, we just inspect the stack directly here. The outermost frame is
  # always the same when this code is invoked by the web server: it is the main
  # request handling function the is invoked in mod_python. In this stack frame
  # the local variable "options" contains the PythonOptions set in the apache
  # config. We get it in this utility function and pass it back so it is
  # avaialable to all code in a thread-safe, non-messy way.

  outermost_frame = inspect.stack()[-1][0] 
  # -1 meaning the last thing in list, i.e., the outermost frame, and 0 meaning
  # that the first thing in the tuple representing the frame is the actual frame
  # object itself which is what we need.

  return outermost_frame.f_locals.get('options')
  # will return None if no options, else options is a dict


def hostname():
  po = passed_options()
  if po and po.has_key('VHOST'):
    return passed_options()['VHOST']
  else:  
    import socket
    return socket.gethostname()


def reload_time():
  try:
    return os.path.getmtime(RELOAD_TIME_FILE_NAME)
  except OSError:
    return 0
  

# having these globals here works because modpython creates a
# separate python sub-interpreter for each virtual host in the
# apache config file
RELOAD_TIME_FILE_NAME = '/var/www/' + hostname() + '_reload_time'

CONFIG_FILE_NAME = '/var/www/' + hostname() + '_config.yml'
config_dict = yaml.load(open(CONFIG_FILE_NAME))
