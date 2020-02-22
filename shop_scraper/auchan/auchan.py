import logging
from time import sleep, time

from funcy.flow import retry
from requests_html import HTMLSession
from requests.exceptions import RequestException

from shop import Shop


session = HTMLSession()
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


class Auchan(Shop):

    def __init__(self, leafpages=None):
        super().__init__(leafpages)

    @property
    def data_dict(self):
        return data_dict

    def collect_leafpages(self, url=None):
        try:
            if url:
                r = session.get(url)
            else:
                r = session.get(self.config['start_url'])
            category_links = self._get_category_links(r)
            sleep(self.config['delay'])
            if not r.html.find('#product_list'):
                for category_link in category_links:
                    self.collect_leafpages(category_link)
            else:
                self.leafpages.add(r.url)
                logging.info('%s added to the leafpages list', r.url)
        except Exception as ex:
            logging.error('The following exception occurred during a product on page %s: %s', url, ex)

    @staticmethod
    def _get_category_links(r):
        """Filters the links, and only category links are returned"""
        return list(filter(
            lambda link: '/shop/catalog/' in link                       # kiszűri a random linkeket
                         and '?' not in link                            # ezt már nem tudom miért raktam bele xd
                         and link.count('/') == r.url.count('/') + 1,   # hogy ne ugorjon 2 kategóráit
            r.html.absolute_links))

    @staticmethod
    def get_html(url):
        r = session.get(url + '?itemsPerPage=5000')
        return r.html

    @retry(5, RequestException)
    def scrape_leafpage(self, html, url):
        try:
            logging.info('Scraping site %s', url)
            category = self.config['base_url'][1].split('?')[0]
            product_list = html.find('#product_list', first=True)
            if not product_list:
                return
            products = product_list.find('.product-card-wrapper')
            for index, product in enumerate(products):
                try:
                    image_box, name_box, price_box = product.find('.box')  # needs refactoring
                    name_str = name_box.find('.productCardPbImg', first=True).attrs['data-product-name']
                    link_str = name_box.find('.productCardPbImg', first=True).attrs['data-product-url']
                    old_price_str = price_box.find('.old-price', first=True).text
                    discount = True if old_price_str else False
                    price_str = price_box.find('.current-price', first=True).find('.price', first=True).text
                    unit_price_price = price_box.find('.unit-price', first=True).find('.unittype')[0].text
                    unit_price_unit = price_box.find('.unit-price', first=True).find('.unittype')[1].text
                    self.data_dict['Name'].append(name_str)
                    self.data_dict['Price'].append(price_str)
                    self.data_dict['Discount'].append(discount)
                    self.data_dict['Unit_price'].append(unit_price_price)
                    self.data_dict['Unit_type'].append(unit_price_unit)
                    self.data_dict['Category'].append(category)
                    self.data_dict['Link'].append(link_str)
                    self.data_dict['Store'].append('Auchan')
                except Exception as ex:
                    logging.error('The following exception occurred during scraping '
                                  'the product in position %s (from %s items), on page %s: %s',
                                  str(index + 1), str(len(products)), url, ex)
                    with open(f'error.{time()}.error.html', 'w') as f:
                        f.write(html.html)
        except RequestException as ex:
            logging.error('The following exception occurred during the request %s: %s', url, ex)
        except Exception as ex:
            logging.error('The following exception occurred during a product on page %s: %s', url, ex)
