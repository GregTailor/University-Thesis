import logging
import re

import requests
from bs4 import BeautifulSoup

from shop import Shop


class Tesco(Shop):

    def __init__(self):
        super().__init__()

    def collect_page_urls(self):
        try:
            r = requests.get(self.shop_config['sitemap'])
            links = re.finditer(r'<loc>(.*)</loc>', r.text)
            sites = []
            for link in links:
                sites.append(link.group(1))
            for site in sites:
                if site[-3:] != 'all' and len(tuple(re.finditer(site, str(sites)))) == 1:
                    self.leafpages.append(site)
        except Exception as ex:
            logging.error('The following exception occurred during sitemap parsing: %s', ex)

    @staticmethod
    def get_html(url):
        r = requests.get(url)
        if not r.ok:
            raise Exception('Response code of the request was not 200')
        return r.text

    def scrape_page(self, html_text, url):
        try:
            html = BeautifulSoup(html_text, 'html.parser')
            category = html.find('h1', {'class': 'heading'}).get_text().encode(encoding='UTF-8', errors='strict')
            logging.info(f'Category name on the page: {category}')

            # Get the number of pages
            paginaton_nav = html.find('nav', {'class': 'pagination--page-selector-wrapper'})
            paginaton_bar = paginaton_nav.find('ul')
            pagination_buttons = paginaton_bar.find_all('li')

            number_of_pages = int(pagination_buttons[-2].text)
            logging.info(f'Number of pages: {number_of_pages}')

            no_of_items = html.find('span', {'class': 'items-count__filter-caption'})
            logging.info(f'No of items: {no_of_items.text}')

            for page_number in range(1, number_of_pages + 1):
                # Get the products on a page
                if number_of_pages > 1:
                    html = BeautifulSoup((requests.get(f'{url}?page={page_number}')).text, 'html.parser')

                logging.info(f'Current page is {url}?page={page_number}')

                unordered_list = html.find('ul', {'class': 'product-list grid'})
                products = unordered_list.find_all('li', {'class': 'product-list--list-item'})

                logging.info('Starting to gather the items from this page')
                for index, product in enumerate(products):
                    logging.info('Scraping product number %s', str(index + 1))
                    # Get the name of the item
                    name = 'null'
                    try:
                        name_link = product.find("a", {'data-auto': 'product-tile--title'})
                        if name_link:
                            name = name_link.text.encode(encoding='UTF-8', errors='strict')

                        # Get the prices of the item
                        price = None
                        price_per_unit = None
                        prices = product.find_all("span", {'class': 'value'})
                        if prices:
                            price = int(prices[0].text.replace(' ', ''))
                            price_per_unit = int(prices[1].text.replace(' ', ''))

                        # Get the measurement
                        measurement = product.find('span', {'class': 'weight'})
                        if measurement:
                            measurement = measurement.text.encode(encoding='UTF-8', errors='strict')

                        discount_f = product.find("div", {'class': 'icon-offer-flash-group'})
                        if discount_f:
                            discount = True
                        else:
                            discount = False

                        product_link = None
                        if name_link:
                            product_link = name_link['href'].encode(encoding='UTF-8', errors='strict')
                        self.to_sql(name, price, discount, price_per_unit, measurement, category, product_link, 'Tesco')
                    except Exception as ex:
                        logging.error('The following exception occured during the scraping of the product number %s named %s: %s', name, str(index + 1), ex)
        except Exception as ex:
            logging.error('The following exception occurred during scraping: %s', ex)
