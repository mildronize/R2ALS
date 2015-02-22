from r2als.libs.functions import extract_grade_subject

__author__ = 'mildronize'

from random import randint

from r2als.libs.logs import Log
from r2als.libs.functions import *
import copy
from r2als.libs.next_solution_methods import *
from r2als.libs.available_semesters import get_available_semesters
from r2als.libs.validators.grade_subject_in_curriculum import is_correct_semester

l = Log('nsm.random_subject_with_rules').getLogger()

class RandomSubjectWithRules(NextSolutionMethod):

    def get_solution(self):
        # 1 random a semester_id(A) /
        # 2 random a subject(A) in semester_id(A)
        #       3. get_available_semesters()
        #       4. random semester(B) in get_available_semesters()
        #       5. random a subject(B) in condition following
        #             if the subject(B) can be enrolled in semester_id(A)
        #                   SWAPPING (Try to swap, if not move it)
        #             else  MOVING

        # 1
        semester_id_0 = self.__random_semester_id()
        # 2
        subject_pos_0 = randint(0, len(self.solution.semesters[semester_id_0].subjects) - 1)
        grade_subject_0 = self.solution.semesters[semester_id_0].subjects[subject_pos_0]

        # 3
        available_semesters = get_available_semesters(self.solution, grade_subject_0)
        # for available_semester in available_semesters:
        #     l.info("available_semester %d/%d" % (self.si.toYear(available_semester), self.si.toSemester(available_semester)))

        # 4
        isMoveSubject = True
        semester_id_1 = 0
        if len(available_semesters) > 0:
            l.info("len(available_semesters) = " + str(len(available_semesters)))

            semester_id_1 = self.__random_semester_id(available_semesters)
            if semester_id_1 >= 0:
                # 5
                available_subjects = copy.copy(self.solution.semesters[semester_id_1].subjects)
                while len(available_subjects) > 0:
                    subject_pos_1 = randint(0, len(available_subjects) - 1)
                    grade_subject_1 = self.solution.semesters[semester_id_1].subjects[subject_pos_1]
                    if is_correct_semester(self.solution, grade_subject_1):
                        isMoveSubject = False
                        break
                    else:
                        available_subjects.pop(subject_pos_1)

                if isMoveSubject:
                    # l.warn("Preparing to move subect " + extract_grade_subject(grade_subject_0))
                    if len(available_semesters) > 0:
                        self.move_grade_subject(grade_subject_0, semester_id_1)
                    else:
                        l.warn("Can't find suitable semester for " + extract_grade_subject(grade_subject_0))
                else:
                    # l.info("Swapping.. "+extract_grade_subject(grade_subject_0) + " with")
                    # l.info("Swapping.. "+extract_grade_subject(grade_subject_1) )
                    self.swap_grade_subject(grade_subject_0, grade_subject_1)
        else:
            # l.warn("Preparing to move subject " + extract_grade_subject(grade_subject_0))
            l.error("can't find available_semesters for " + extract_grade_subject(grade_subject_0))
            return Nones
        return self.solution

    def __random_semester_id(self, external_available_semesters=None):
        available_semesters = self.__find_not_empty_semester_ids(external_available_semesters)
        if len(available_semesters) == 0:
            return -1

        return available_semesters[randint(0, len(available_semesters)-1)]

    def __find_not_empty_semester_ids(self, external_available_semesters=None):
        available_semesters = []
        if external_available_semesters is None:
            for semester_id in range(self.solution.member.num_studied_semester_id,
                                     len(self.solution.semesters)):
                if len(self.solution.semesters[semester_id].subjects) != 0:
                    available_semesters.append(semester_id)
        else:
            for semester_id in external_available_semesters:
                if len(self.solution.semesters[semester_id].subjects) != 0:
                    available_semesters.append(semester_id)
        return available_semesters