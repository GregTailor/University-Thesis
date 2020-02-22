import logging
from abc import ABC, abstractmethod

import pandas

from helper import get_config


config = get_config()


class Shop(ABC):

    def __init__(self, leafpages=None):
        self.config = config[self.__class__.__name__.lower()]
        self.leafpages = set() if not leafpages else leafpages
        self.df = pandas.DataFrame()

    @property
    @abstractmethod
    def data_dict(self):
        pass

    def __repr__(self):
        return ''

    def _scrape(self):
        """Collects all the leafpages and scrape every leafpage, thus filling the Dataframe"""
        if not self.leafpages:
            self.collect_leafpages()
            logging.info('The leafpages are collected')

        for page_url in self.leafpages:
            try:
                html = self.get_html(page_url)
                self.scrape_leafpage(html, page_url)
            except Exception as ex:
                logging.error('Unexpected error occurred during scraping page %s: %s', page_url, ex)

    @abstractmethod
    def collect_leafpages(self):
        """Collects the leafpages, by appending them to self.leafpages"""
        pass

    @staticmethod
    @abstractmethod
    def get_html(url):
        """

        Sends a request to the given url
        the return is r.text for BeautifulSoup
        the return is r.html for requests-html

        """
        pass

    @abstractmethod
    def scrape_leafpage(self, html, url):
        """Scrapes the html, and appends the results to self.data_dict"""
        pass

    def scrape(self):
        logging.info('The scraping for shop %s started', self.__class__.__name__)

        self._scrape()

        logging.info('The scraping for shop %s finished', self.__class__.__name__)

        df = pandas.DataFrame(self.data_dict)
        self.df = df
        self.df.drop_duplicates(subset=['Name', 'Price', 'Unit_price', 'Unit_type', 'Category', 'Store'])
        logging.info('Pandas dataframe created for shop %s', self.__class__.__name__)

        return self.df

    def to_excel(self, filename):
        if filename[-5:] != '.xlsx':
            filename += '.xlsx'
        self.df.to_excel(filename)
