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
        date_range = len(self._date_options())
        self.student.timetable = Timetable()
        for index in range(date_range):
            self._select_date(index)
            self._click_submit()
            self._collect_information_date()
        self.browser.close()

    def scrape_by_major_and_year(self):
        if not self.browser:
            self.initialize_browser()
        major_options_str = self._major_options_str()
        self.student.timetable = Timetable()
        for index, major_str in enumerate(major_options_str):
            if major_str in self.student.major_filter:
                self._select_major(index)
                self._click_submit()
                self._collect_information_major()
        self.browser.close()

    def initialize_browser(self):
        self.browser = webdriver.Chrome()
        self.browser.get('https://arato.inf.unideb.hu/levelezo/index.php')

    def scrape(self):
        if self.student.year:
            self.scrape_by_major_and_year()
        else:
            self.scrape_by_date()

    def _date_options(self):
        date_selector = self.browser.find_element_by_css_selector('select[name=datum]')
        return date_selector.find_elements_by_css_selector('option')[1:]

    def _major_options(self):
        major_selector = self.browser.find_element_by_css_selector('select[name=szak]')
        return major_selector.find_elements_by_css_selector('option')[1:]

    def _date_options_str(self):
        return [date_option.text for date_option in self._date_options()]

    def _major_options_str(self):
        return [major_option.text for major_option in self._major_options()]

    def _click_submit(self):
        submit_button = self.browser.find_element_by_css_selector('input[type=submit]')
        submit_button.click()

    def _select_date(self, index):
        self._date_options()[index].click()

    def _select_major(self, index):
        self._major_options()[index].click()

    def _collect_information_date(self):
        table = self.browser.find_element_by_css_selector('table')
        table_rows = table.find_elements_by_css_selector('tr')
        hours_index, subject_name_index, teacher_index, classroom_index = self._get_column_indexes(table_rows)
        date = table_rows.pop(0).find_element_by_css_selector('td').text
        classes = table_rows
        for info in classes:
            class_informations = info.find_elements_by_css_selector('td')
            hours = class_informations[hours_index].text
            subject_name = class_informations[subject_name_index].find_element_by_css_selector('b').text
            subject_code = subject_name.split(' ')[0]
            teacher = class_informations[teacher_index].text
            classroom = class_informations[classroom_index].find_element_by_css_selector('i').text
            if subject_code in self.student.subject_codes:
                self.student.timetable.add_class(Lesson(date, hours, subject_code, subject_name, teacher, classroom))

    def _collect_information_major(self):
        table = self.browser.find_element_by_css_selector('table')
        table_rows = table.find_elements_by_css_selector('tr')
        hours_index, subject_name_index, teacher_index, classroom_index = self._get_column_indexes(table_rows)
        date = None
        for table_row in table_rows:
            table_row_data = table_row.find_elements_by_css_selector('td')
            if len(table_row_data) == 1:
                date = table_row_data[0].text
            else:
                hours = table_row_data[hours_index].text
                subject_name = table_row_data[subject_name_index].find_element_by_css_selector('b').text
                subject_code = subject_name.split(' ')[0]
                teacher = table_row_data[teacher_index].text
                classroom = table_row_data[classroom_index].find_element_by_css_selector('i').text
                if subject_code in self.student.subject_codes:
                    self.student.timetable.add_class(Lesson(date, hours, subject_code, subject_name, teacher, classroom))

    @staticmethod
    def _get_column_indexes(table_rows):
        column_names = [column.text for column in table_rows.pop(0).find_elements_by_css_selector('th')]
        hours_index = column_names.index('Óra')
        subject_name_index = column_names.index('Tantárgy')
        teacher_index = column_names.index('Oktató')
        classroom_index = column_names.index('Terem')
        return hours_index, subject_name_index, teacher_index, classroom_index
