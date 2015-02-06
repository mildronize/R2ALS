from r2als.libs.functions import extract_grade_subject

__author__ = 'mildronize'

from random import randint

from r2als.libs.logs import Log
from r2als.libs.functions import *
from r2als.libs.next_solution_methods import *

l = Log('next_solution_methods.random').getLogger()

class RandomSubject(NextSolutionMethod):

    def get_solution(self):
        semester_id = self.__random_two_semesters()
        subject_pos = self.__random_two_subjects(semester_id[0], semester_id[1])
        l.info("subject_pos" + str(subject_pos))

        grade_subject_0 = self.solution.semesters[semester_id[0]].subjects[subject_pos[0]]
        grade_subject_1 = self.solution.semesters[semester_id[1]].subjects[subject_pos[1]]

        si = SemesterIndex(self.solution.member.curriculum.num_semester)
        if si.get(grade_subject_0.year, grade_subject_0.semester) == semester_id[0]:
            l.info("Correct grade_subject_0")
        else:
            l.error("Incorrect grade_subject_0")
        if si.get(grade_subject_1.year, grade_subject_1.semester) == semester_id[1]:
            l.info("Correct grade_subject_1")
        else:
            l.error("Incorrect grade_subject_1")

        extract_grade_subject(grade_subject_0)
        extract_grade_subject(grade_subject_1)

        from r2als.engines.tabu_handler import TabuHandler
        tabu = TabuHandler(10)
        tabu.add_next_solution(self.solution)
        self.swap_grade_subject(grade_subject_0, grade_subject_1)
        # self.solution.semesters[semester_id[0]].subjects.pop(0)
        tabu.add_next_solution(self.solution)
        return self.solution

    def __random_two_semesters(self):
        semester_id =  self.__random_two_things(rand_start=self.solution.member.num_studied_semester_id,
                                                rand_end=len(self.solution.semesters))
        l.info("semester_id" + str(semester_id))
        while len(self.solution.semesters[semester_id[0]].subjects) == 0 or \
            len(self.solution.semesters[semester_id[1]].subjects) == 0 or semester_id[0] == semester_id[1]:
            semester_id =  self.__random_two_things(rand_start=self.solution.member.num_studied_semester_id,
                                                    rand_end=len(self.solution.semesters))
        return semester_id

    def __random_two_subjects(self, semester_id_0, semester_id_1):
        l.info("sem "+str(semester_id_0)+": " + str(len(self.solution.semesters[semester_id_0].subjects)))

        l.info("sem "+str(semester_id_1)+": " + str(len(self.solution.semesters[semester_id_1].subjects)))
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