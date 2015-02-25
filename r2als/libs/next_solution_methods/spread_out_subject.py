__author__ = 'mildronize'

from r2als.libs.rules import Rule
from r2als import config
from r2als.libs.logs import Log
from r2als.libs.next_solution_methods import *
from r2als.libs.available_semesters import get_available_semesters
l = Log('nsm.move_non_related_subject_out').getLogger()

class SpreadOutSubject(NextSolutionMethod):

    def get_solution(self, random_operator):
        l.info("Move Non Related Subject Out start")
        self.random_operator = random_operator
        self.spread_out_subject()
        return self.solution

    def spread_out_subject(self):

        average_credit = self.__find_average_credit(self.solution.member.num_studied_semester_id, len(self.solution.semesters))
        # todo: Can do faster
        # available_semesters = self.__find_available_semesters()
        semester_id_0 = self.__find_max_credit_of_semester_id(self.solution.member.num_studied_semester_id, len(self.solution.semesters))


    def __find_available_semesters(self):
        return []

    def __find_max_credit_of_semester_id(self, semester_id_start, semester_id_end):
        max = 0
        for semester_id in range(semester_id_start, semester_id_end):
            if self.solution.semesters[max].total_credit < self.solution.semesters[semester_id].total_credit:
                max = semester_id
        return max

    def __find_average_credit(self, semester_id_start, semester_id_end):
        total_credit = 0
        for semester_id in range(semester_id_start, semester_id_end):
            total_credit += self.solution.semesters[semester_id].total_credit
        return total_credit / (semester_id_end - semester_id_start)