from student import Student
from scaper import TimetableScraper


subject_codes = ['ILBPM9934', 'ILBPM9928', 'ILBPM9936', 'ILBPM9924', 'ILBPM0417',
                 'ILBPM0419', 'ILBPM0623', 'ILBPM9925', 'ILBPM0420', 'ILBPM0418']
major = 'PTI BSC'
year = (1, 2, 3)
student = Student('Szabó Gergő', subject_codes, year, major)
scraper = TimetableScraper(student)
student.timetable.print_classes_in_order()
student.timetable.print_classes_by_subjects()
