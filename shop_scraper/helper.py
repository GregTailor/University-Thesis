import logging
import os
from datetime import datetime
from functools import wraps

import yaml
import psycopg2


def get_config(config_path='./config.yaml'):
    with open(config_path, encoding='utf-8') as f:
        config = yaml.load(f)
    return config


def folder_init(config):
    os.makedirs(config['folders']['log'], exist_ok=True)


def logger_init():
    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s')
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    return now, formatter, logger


def get_credentials(credential_path='./credentials.local'):
    with open(credential_path, encoding='utf-8') as f:
        credentials = yaml.load(f)
    return credentials


def create_logger(logger, log_level, formatter, log_file=None):
    if log_file:
        log_handler = logging.FileHandler(filename=log_file, mode='w', encoding='utf-8')
    else:
        log_handler = logging.StreamHandler()
    log_handler.setLevel(log_level)
    log_handler.setFormatter(formatter)
    logger.addHandler(log_handler)


def connect(config, credentials):
    # conn = None
    try:
        logging.info('Connecting to the PostgreSQL database...')
        return psycopg2.connect(host=config['database']['host'], 
                                dbname=config['database']['db_name'], 
                                user=credentials['user'], 
                                password=credentials['password'])
 
    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)


def connect_teardown(conn):
    if conn is not None:
        conn.close()
        logging.info('Database connection closed.')


def log_before_after(log_message_1, log_message_2):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if log_message_1:
                logging.info('%s', log_message_1)
            value = function(*args, **kwargs)
            if log_message_2:
                logging.info('%s', log_message_2)
            return value
        return wrapper
    return real_decorator


def log_before(log_message):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            if log_message:
                logging.info('%s', log_message)
            return function(*args, **kwargs)
        return wrapper
    return real_decorator


def log_after(log_message):
    def real_decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            value = function(*args, **kwargs)
            if log_message:
                logging.info('%s', log_message)
            return value
        return wrapper
    return real_decorator
