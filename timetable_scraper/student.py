class Student:

    def __init__(self, name, subject_codes, year=(), major=None):
        self.name = name
        self.subject_codes = subject_codes
        self.timetable = None
        self.year = year
        self.major = major

    @property
    def major_filter(self):
        if self.major.lower() == 'pti bsc':
            return [f'{year}. Programtervező informatikus BSc' for year in self.year]
        return None
