import logging
import os
from datetime import datetime

# Get the current date and time to use in the log file name
log_filename = 'logs/' + datetime.now().strftime('%Y-%m-%d') + '.log'

# Ensure logs directory exists
os.makedirs('logs', exist_ok=True)

# Set up logging configuration
logging.basicConfig(
    filename=log_filename,
    level=logging.DEBUG,     # Log level to capture all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s,%(process)s %(levelname)s - %(message)s - [%(filename)s:%(lineno)s - %(funcName)s()]'
)

# Create a custom logger
log = logging.getLogger()

