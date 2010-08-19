

import yaml, json


CONFIG_FILE_NAME = '/var/www/config.yml'


def get():
  cfg = yaml.load(open(CONFIG_FILE_NAME))
  return json.dumps(cfg)

