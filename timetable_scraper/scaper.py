from selenium import webdriver

from timetable import Timetable
from lesson import Lesson


class TimetableScraper:

    def __init__(self, student, start_on_creation=True):
        self.student = student
        self.browser = None
        if start_on_creation:
            self.scrape()

    def scrape_by_date(self):
        if not self.browser:
            self.initialize_browser()
        self.student.timetable = Timetable()
        date_selector = self.browser.find_element_by_css_selector('select[name=datum]')
        date_options = date_selector.find_elements_by_css_selector('option')[1:]
        date_options_str = [date_option.text for date_option in date_options]
        for index, date_str in enumerate(date_options_str):
            date_selector = self.browser.find_element_by_css_selector('select[name=datum]')
            submit_button = self.browser.find_element_by_css_selector('input[type=submit]')
            _date_options = date_selector.find_elements_by_css_selector('option')[1:]
            _date_options[index].click()
            submit_button.click()
            table = self.browser.find_element_by_css_selector('table')
            table_rows = table.find_elements_by_css_selector('tr')
            classes = table_rows[2:]
            for info in classes:
                class_informations = info.find_elements_by_css_selector('td')
                hours = class_informations[0].text
                subject_name = class_informations[3].find_element_by_css_selector('b').text
                subject_code = subject_name.split(' ')[0]
                if subject_code in self.student.subject_codes:
                    self.student.timetable.add_class(Lesson(date_str, hours, subject_code, subject_name))
        self.browser.close()

    def scrape_by_year(self):
        pass

    def initialize_browser(self):
        self.browser = webdriver.Chrome()
        self.browser.get('https://arato.inf.unideb.hu/levelezo/index.php')

    def scrape(self):
        if self.student.year:
            self.scrape_by_year()
        else:
            self.scrape_by_date()
