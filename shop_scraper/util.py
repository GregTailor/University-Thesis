import json
import logging
from datetime import datetime


def get_config(filename):
    with open(filename, encoding='utf-8') as f:
        return json.load(f)


def logger_configurations():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{now}.log"
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return filename, formatter, logger


def create_logger(logger, log_level, formatter, log_file=None):
    if log_file:
        log_handler = logging.FileHandler(filename=log_file, mode='w', encoding='utf-8')
    else:
        log_handler = logging.StreamHandler()
    log_handler.setLevel(log_level)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)
