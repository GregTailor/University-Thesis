class Student:

    def __init__(self, name, subject_codes, year=()):
        self.name = name
        self.subject_codes = subject_codes
        self.timetable = None
        self.year = year
