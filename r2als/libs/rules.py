__author__ = 'Thada Wangthammang'

class Rule:

    def __init__(self, member):
        self.member = member
        self.maximum_credit = {
            'regular_semester_and_regular_student': 22,
            'regular_semester_and_critical_student': 16,
            'summer_semester_and_regular_student': 9,
            'summer_semester_and_critical_student': 6
        }

    def calculate_maximum_credit(self, semester_id):
        return self.maximum_credit['regular_semester_and_regular_student'] #+ self.member.margin_credit
