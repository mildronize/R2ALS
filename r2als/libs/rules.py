__author__ = 'Thada Wangthammang'

from r2als.libs.functions import SemesterIndex

class Rule:

    def __init__(self, member):
        self.si = SemesterIndex(member.curriculum.num_semester)
        self.member = member
        self.maximum_credit = {
            'regular_semester_and_regular_student': 22,
            'regular_semester_and_critical_student': 16,
            'summer_semester_and_regular_student': 9,
            'summer_semester_and_critical_student': 6
        }

    def calculate_maximum_credit(self, semester_id):
        if self.si.toSemester(semester_id) == 3:
            return self.maximum_credit['summer_semester_and_regular_student']
        return self.maximum_credit['regular_semester_and_regular_student'] #+ self.member.margin_credit
