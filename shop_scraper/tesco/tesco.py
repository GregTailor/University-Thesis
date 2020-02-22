import logging
import re

import requests
from bs4 import BeautifulSoup

from shop import Shop


data_dict = {
            'Name': [],
            'Price': [],
            'Discount': [],
            'Unit_price': [],
            'Unit_type': [],
            'Category': [],
            'Link': [],
            'Store': []
        }


class Tesco(Shop):

    def __init__(self, leafpages=None):
        super().__init__(leafpages)

    @property
    def data_dict(self):
        return data_dict

    def collect_leafpages(self):
        try:
            r = requests.get(self.config['sitemap'])
            links = re.finditer(r'<loc>(.*)</loc>', r.text)
            sites = []
            for link in links:
                sites.append(link.group(1))
            for site in sites:
                if site[-3:] != 'all' and len(tuple(re.finditer(site, str(sites)))) == 1:
                    self.leafpages.add(site)
        except Exception as ex:
            logging.error('The following exception occurred during sitemap parsing: %s', ex)

    @staticmethod
    def get_html(url):
        r = requests.get(url)
        if not r.ok:
            raise Exception('Response code of the request was not 200')
        return r.text

    def scrape_leafpage(self, html, url):
        try:
                soup = BeautifulSoup(html, 'html.parser')

                category = soup.find('h1', {'class': 'heading query'})
                logging.info(f'Category name on the page: {category.text}')

                # Get the number of pages
                paginaton_nav = soup.find('nav', {'class': 'pagination--page-selector-wrapper'})
                paginaton_bar = paginaton_nav.find('ul')
                pagination_buttons = paginaton_bar.find_all('li')

                number_of_pages = int(pagination_buttons[-2].text)
                logging.info(f'Number of pages: {number_of_pages}')

                no_of_items = soup.find('span', {'class': 'items-count__filter-caption'})
                logging.info(f'No of items: {no_of_items.text}')

                for page_number in range(1, number_of_pages + 1):
                    # Get the products on a page
                    if number_of_pages > 1:
                        soup = BeautifulSoup((requests.get(f'{url}?page={page_number}')).text, 'html.parser')

                    logging.info(f'Current page is {url}?page={page_number}')

                    unordered_list = soup.find('ul', {'class': 'product-list grid'})
                    products = unordered_list.find_all('li', {'class': 'product-list--list-item'})

                    logging.info('Starting to gather the items from this page')
                    for product in products:
                        # Get the name of the item
                        name = None
                        name_link = product.find("a", {'class': 'product-tile--title product-tile--browsable'})
                        if name_link:
                            name = name_link.text

                        # Get the prices of the item
                        price_main = None
                        price_per_unit = None
                        prices = product.find_all("span", {'class': 'value'})
                        if prices:
                            price_main = prices[0].text
                            price_per_unit = prices[1].text

                        # Get the measurement
                        measurement = product.find('span', {'class': 'weight'})
                        if measurement:
                            measurement = measurement.text

                        discount_f = product.find("div", {'class': 'icon-offer-flash-group'})
                        if discount_f:
                            discount = 'true'
                        else:
                            discount = 'false'

                        product_link = None
                        product_link_pre = product.find("a", {'class': 'product-tile--title product-tile--browsable'})
                        if product_link_pre:
                            product_link = product_link_pre['href']

                        self.data_dict['Name'].append(name)
                        self.data_dict['Price'].append(price_main)
                        self.data_dict['Discount'].append(discount)
                        self.data_dict['Unit_price'].append(price_per_unit)
                        self.data_dict['Unit_type'].append(measurement)
                        self.data_dict['Category'].append(category.text)
                        self.data_dict['Link'].append(product_link)
                        self.data_dict['Store'].append('Tesco')
        except Exception as ex:
            logging.error('The following exception occurred during scraping: %s', ex)
