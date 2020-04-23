import logging
from abc import ABC, abstractmethod
from datetime import datetime

from sqlalchemy import engine, MetaData, Table, Column, String, DateTime, Integer, Boolean

from util import get_config


class Shop(ABC):

    database_configuration = get_config('database_config.json')
    config = get_config('config.json')

    def __init__(self):
        self.shop_config = self.config[self.__class__.__name__.lower()]
        self.number_of_pages_to_scrape = self.shop_config['number_of_pages_to_scrape']
        self.scrape_date = None
        self.leafpages = []
        self.database_engine = engine.create_engine('mysql://root:admin@localhost/shopscraper')
        self.database_metadata = MetaData(self.database_engine)
        self.database_table_exists = True if self.__class__.__name__.lower() in self.database_engine.table_names() else False
        self.database_table = None
        self.database_connection = None

    @abstractmethod
    def collect_page_urls(self):
        pass

    @staticmethod
    @abstractmethod
    def get_html(url):
        pass

    @abstractmethod
    def scrape_page(self, html, url):
        pass

    def scrape(self):
        self.scrape_date = datetime.now()  # .strftime("%Y%m%d_%H%M%S")

        if not self.database_table_exists:
            self.database_table_does_not_exist()
        logging.info('The scraping for shop %s started', self.__class__.__name__)
        logging.info('Number of pages to scrape: %s',
                     str(self.number_of_pages_to_scrape) if self.number_of_pages_to_scrape > 0 else 'all')

        self.collect_page_urls()
        logging.info('The leafpages are collected')
        self.database_table = Table(self.__class__.__name__.lower(), self.database_metadata,
                                    autoload=True, autoload_with=self.database_engine)
        self.database_connection = self.database_engine.connect()
        while self.leafpages and self.number_of_pages_to_scrape != 0:
            page_url = self.leafpages.pop()
            try:
                html = self.get_html(page_url)
                self.scrape_page(html, page_url)
                self.number_of_pages_to_scrape = self.number_of_pages_to_scrape - 1
            except Exception as ex:
                logging.error('Unexpected error occurred during scraping page %s: %s', page_url, ex)
        self.database_connection.close()
        logging.info('The scraping for shop %s finished', self.__class__.__name__)

    def to_sql(self, name, price, discount, unit_price, unit_type, category, link, store):
        if self.database_table is not None and self.database_connection is not None:
            insert_command = self.database_table.insert().values(name=name, date=self.scrape_date, price=price,
                                                                 discount=discount, unit_price=unit_price,
                                                                 unit_type=unit_type, category=category,
                                                                 link=link, store=store)
            self.database_connection.execute(insert_command)

    def database_table_does_not_exist(self):
        self.create_table()

    def create_table(self):
        Table(self.__class__.__name__.lower(), self.database_metadata,
              Column('name', String(256), primary_key=True),
              Column('date', DateTime, primary_key=True),
              Column('price', Integer),
              Column('discount', Boolean),
              Column('unit_price', Integer),
              Column('unit_type', String(64)),
              Column('category', String(256)),
              Column('link', String(256)),
              Column('store', String(256)))
        self.database_metadata.create_all()
