import datetime


class Lesson:

    def __init__(self, date, hours, subject_code, subject_name, teacher, classroom):
        self.date = date
        self.hours = hours
        self.start_hour = int(hours.split('-')[0].replace(':00', ''))
        self.end_hour = hours.split('-')[1].replace(':00', '')
        self.subject_code = subject_code
        self.subject_name = subject_name.replace(f'{subject_code} ', '')[:-1]
        self.teacher = teacher
        self.classroom = classroom
        self.sortable_date = f'{str(datetime.datetime.now().year)} {date}'.replace('január', '1')\
            .replace('február', '2')\
            .replace('március', '3')\
            .replace('április', '4')\
            .replace('május', '5')\
            .replace('június', '6')\
            .replace('július', '7')\
            .replace('augusztus', '8')\
            .replace('szeptember', '9')\
            .replace('október', '10')\
            .replace('november', '11')\
            .replace('december', '12').replace(' (csütörtök)', '').replace(' (péntek)', '').replace(' (szombat)', '')

    def __str__(self):
        return f'{self.date} {self.start_hour} - {self.end_hour}: {self.subject_name} - {self.teacher} | {self.classroom} |'
