__author__ = 'mildronize'

from r2als.libs.functions import SemesterIndex
from r2als.libs.logs import Log

l = Log('Filter').getLogger()

class Filter:

    def __init__(self, solutions):
        print("running Filter")
        self.solutions = solutions
        self.si = SemesterIndex(solutions[0].member.curriculum.num_semester)

        self.EXPECTED_GRADUATE_SEMESTER = self.si.get(5,1)
        self.MAX_CALC_SUBJECT_PER_SEMESTER = 1
        self.MAX_ENGLISH_SUBJECT_PER_SEMESTER = 1
        # self.si = SemesterIndex(self.member.curriculum.num_semester)

    def start(self):
        l.info("start")
        i = 0
        for solution in self.solutions:
            solution.conditions = self.filter_solution(solution)
            i+=1
            l.info("solution %d: %s"% (i,list(solution.conditions)))
            # l.info("max-> %d" % self.count_subject_with_tag_per_semester(solution,'calculation')['max'])
            # l.info("max-> %d" % self.count_subject_with_tag_per_semester(solution,'calculation')['max_semester'])
        return self.solutions

    def filter_solution(self, solution):
        tmp = []
        if len(solution.semesters) <= self.EXPECTED_GRADUATE_SEMESTER:
            tmp.append(1)
        else:
            tmp.append(0)

        if self.count_subject_with_tag_per_semester(solution,'calculation')['max'] \
                <= self.MAX_CALC_SUBJECT_PER_SEMESTER:
            tmp.append(1)
        else:
            tmp.append(0)

        if self.count_subject_with_tag_per_semester(solution,'english')['max'] \
                <= self.MAX_CALC_SUBJECT_PER_SEMESTER:
            tmp.append(1)
        else:
            tmp.append(0)
        return tmp

    def count_subject_with_tag_per_semester(self, solution, tag_name):
        total = {
            'min': 9999,
            'max': 0
        }
        for semester in solution.semesters:
            num_subjects = 0
            for grade_subject in semester.subjects:
                if tag_name in grade_subject.subject.tags:
                    num_subjects += 1
            if num_subjects < total['min']:
                total['min'] = num_subjects
                total['min_semester'] = self.si.get(semester.year, semester.semester)
            if num_subjects > total['max']:
                total['max'] = num_subjects
                total['max_semester'] = self.si.get(semester.year, semester.semester)
        return total



