class Lesson:

    def __init__(self, date, hours, subject_code, subject_name):
        self.date = date
        self.hours = hours
        self.start_hour = int(hours.split('-')[0].replace(':00', ''))
        self.end_hour = hours.split('-')[1].replace(':00', '')
        self.subject_code = subject_code
        self.subject_name = subject_name.replace(f'{subject_code} ', '')[:-1]

    def __str__(self):
        return f'{self.date} {self.start_hour} - {self.end_hour}: {self.subject_name}'
