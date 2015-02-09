from r2als.libs.functions import extract_grade_subject

__author__ = 'mildronize'

from random import randint

from r2als.libs.logs import Log
from r2als.libs.functions import *
from r2als.libs.next_solution_methods import *

l = Log('nsm.random_subject_with_rules').getLogger()

class RandomSubjectWithRules(NextSolutionMethod):

    def get_solution(self):





        return self.solution

    def __random_two_semesters(self):
        semester_id =  self.__random_two_things(rand_start=self.solution.member.num_studied_semester_id,
                                                rand_end=len(self.solution.semesters))
        # l.info("semester_id" + str(semester_id))
        while len(self.solution.semesters[semester_id[0]].subjects) == 0 or \
            len(self.solution.semesters[semester_id[1]].subjects) == 0 or semester_id[0] == semester_id[1]:
            semester_id =  self.__random_two_things(rand_start=self.solution.member.num_studied_semester_id,
                                                    rand_end=len(self.solution.semesters))
        return semester_id

    def __random_two_subjects(self, semester_id_0, semester_id_1):
        # l.info("sem "+str(semester_id_0)+": " + str(len(self.solution.semesters[semester_id_0].subjects)))
        # l.info("sem "+str(semester_id_1)+": " + str(len(self.solution.semesters[semester_id_1].subjects)))
        return [
            self.__random_two_things(rand_start=0, rand_end=len(self.solution.semesters[semester_id_0].subjects))[0],
            self.__random_two_things(rand_start=0, rand_end=len(self.solution.semesters[semester_id_1].subjects))[0]
        ]

    def __random_two_things(self, rand_start, rand_end):
        thing_1 = -1
        thing_2 = -1
        diff = rand_end - rand_start
        rand_end -= 1
        if diff == 1:
            if randint(0,1) == 1:
                return [rand_start, rand_end]
            return [rand_end, rand_start]
        elif diff > 1:
            thing_1 = randint(rand_start, rand_end)
            thing_2 = randint(rand_start, rand_end)
        else:
            thing_1 = rand_start
        return [thing_1, thing_2]