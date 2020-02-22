from lesson import Lesson


class Timetable:

    def __init__(self):
        self.classes = []

    @property
    def subject_codes(self):
        return set([class_.subject_code for class_ in self.classes])

    def add_class(self, class_):
        if isinstance(class_, Lesson):
            self.classes.append(class_)
        else:
            raise Exception

    def print_classes_in_order(self):
        for class_ in self.classes:
            print(class_)

    def print_classes_by_subjects(self):
        for subject_code in self.subject_codes:
            for class_ in self.classes:
                if class_.subject_code == subject_code:
                    print(class_)
