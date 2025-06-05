import logging
from datetime import datetime

LOG_FILE = 'smartpath.log'

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_action(user_id, action, details=None):
    msg = f"User {user_id} ACTION: {action}"
    if details:
        msg += f" | Details: {details}"
    logging.info(msg)

def log_error(user_id, error, details=None):
    msg = f"User {user_id} ERROR: {error}"
    if details:
        msg += f" | Details: {details}"
    logging.error(msg) 