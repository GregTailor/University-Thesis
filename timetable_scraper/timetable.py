from datetime import datetime

from lesson import Lesson


class Timetable:

    def __init__(self):
        self.lessons = []

    @property
    def subject_codes(self):
        return set([class_.subject_code for class_ in self.lessons])

    def add_class(self, class_):
        if isinstance(class_, Lesson):
            self.lessons.append(class_)
        else:
            raise Exception

    def print_classes_in_order(self):
        ordered_classes = self.lessons
        ordered_classes.sort(key=lambda lesson: datetime.strptime(lesson.sortable_date, '%Y %m %d'))
        for class_ in ordered_classes:
            print(class_)

    def print_classes_by_subjects(self):
        for subject_code in self.subject_codes:
            for class_ in self.lessons:
                if class_.subject_code == subject_code:
                    print(class_)
