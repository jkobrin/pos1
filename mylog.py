
import glob
import logging
import logging.handlers

LOG_FILENAME = '/var/www/pos.log'

# Set up a specific logger with our desired output level
my_logger = logging.getLogger('MyLogger')
my_logger.setLevel(logging.DEBUG)

# Create log message handler
handler = logging.handlers.RotatingFileHandler(
              LOG_FILENAME, maxBytes=200000, backupCount=5)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to handler
handler.setFormatter(formatter)

# Add the log message handler to the logger
my_logger.addHandler(handler)


if __name__ == '__main__':
  my_logger.debug('hi there')
