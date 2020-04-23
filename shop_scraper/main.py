import logging

from util import logger_configurations, create_logger
from tesco import Tesco


def initialize_logging():
    name, formatter, logger = logger_configurations()
    create_logger(logger, logging.INFO, formatter, name)


def main():
    initialize_logging()
    tesco = Tesco()
    tesco.scrape()


if __name__ == '__main__':
    main()
