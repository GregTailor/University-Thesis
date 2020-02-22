import logging
import argparse

from helper import folder_init, logger_init, create_logger, get_config
from auchan.auchan import Auchan
from tesco.tesco import Tesco


def init(config):
    folder_init(config)
    now, formatter, logger = logger_init()
    # create_logger(logger, logging.INFO, formatter, f'{config["folders"]["log"]}/{now}_info_log.txt')
    # create_logger(logger, logging.ERROR, formatter, f'{config["folders"]["log"]}/{now}_error_log.txt')
    create_logger(logger, logging.INFO, formatter)
    return now


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-tesco', action='store_true')
    parser.add_argument('-auchan', action='store_true')
    return parser.parse_args()


def main():
    config = get_config()
    now = init(config)
    args = get_arguments()

    # old:
    # if args.tesco:
    #     logging.info('Tesco Scraper has starterd')
    #     df = scrape_tesco(config)
    #     df = df.drop_duplicates(subset=['Name', 'Price', 'Unit_price', 'Unit_type', 'Category', 'Store'])
    #     df.to_excel(f"Tesco_{now}.xlsx")
    #
    # if args.auchan:
    #     logging.info('Auchan Scraper has started')
    #     df = scrape_auchan(config['auchan'])
    #     df = df.drop_duplicates(subset=['Name', 'Price', 'Unit_price', 'Unit_type', 'Category', 'Store'])
    #     df.to_excel(f'Auchan_{now}.xlsx')
    # new:
    if args.auchan:
        auchan = Auchan()
        auchan.scrape()  # the config load can be found in the Shop class
        auchan.to_excel(f'Auchan_{now}')    # the to_excel function belongs to the
                                            # Auchan class, and appends .xlsx in the end if it's not present
                                            # also the df.drop_duplicates is implemented inside the shop class
    if args.tesco:
        tesco = Tesco()
        tesco.scrape()
        tesco.to_excel(f'Tesco_{now}')


if __name__ == '__main__':
    main()
