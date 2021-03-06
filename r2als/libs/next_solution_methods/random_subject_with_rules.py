from r2als.libs.functions import extract_grade_subject

__author__ = 'mildronize'

from r2als.libs.logs import Log
from r2als.libs.functions import *
from r2als import config
import copy
from r2als.libs.next_solution_methods import *
from r2als.libs.available_semesters import get_available_semesters
from r2als.libs.validators.grade_subject_in_curriculum import is_correct_semester

l = Log('nsm.random_subject_with_rules').getLogger()

class RandomSubjectWithRules(NextSolutionMethod):

    def get_solution(self, random_operator):
        is_add_extra_semester = False
        self.random_operator = random_operator
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
        available_subjects = self.__get_available_subjects(semester_id_0)
        # grade_subject_0 = self.random_operator.randint(0, len(available_subjects) - 1)
        if len(available_subjects) == 0:
            l.error("sth error")
            return None
        subject_pos_0 = available_subjects[self.random_operator.randint(0, len(available_subjects) - 1)]
        grade_subject_0 = self.solution.semesters[semester_id_0].subjects[subject_pos_0]
        l.debug("grade_subject_0 >> " + extract_grade_subject(grade_subject_0))
        # subject_pos_0 = self.random_operator.randint(0, len(self.solution.semesters[semester_id_0].subjects) - 1)
        # grade_subject_0 = self.solution.semesters[semester_id_0].subjects[subject_pos_0]

        # 3
        available_semesters = get_available_semesters(self.solution, grade_subject_0)
        # extra semester
        if is_add_extra_semester:
            new_year = self.si.toYear(self.solution.min_semester_id) + 1
            new_semester = grade_subject_0.semester
            new_semester_id = self.si.get(new_year, new_semester)
            if new_semester_id not in available_semesters:
                available_semesters.append(new_semester_id)
        # for available_semester in available_semesters:
        #     l.info("available_semester %d/%d" % (self.si.toYear(available_semester), self.si.toSemester(available_semester)))

        # 4
        isMoveSubject = True

        # semester_id_1 = 0
        if len(available_semesters) > 0:
            # l.info("len(available_semesters) = " + str(len(available_semesters)))

            semester_id_1 = self.__random_semester_id(available_semesters)
            if semester_id_1 >= 0:
                # 5
                available_subjects = self.__get_available_subjects(semester_id_1)
                l.info("available_subjects of "+extract_grade_subject(grade_subject_0))
                for available_subject in available_subjects:
                    l.debug("%d) %s" % (available_subject ,extract_grade_subject(self.solution.semesters[semester_id_1].subjects[available_subject])))
                while len(available_subjects) > 0:
                    subject_pos_1 = available_subjects[self.random_operator.randint(0, len(available_subjects) - 1)]
                    grade_subject_1 = self.solution.semesters[semester_id_1].subjects[subject_pos_1]
                    # l.info("%d) %s" % (subject_pos_1 ,extract_grade_subject(grade_subject_1)))
                    if is_correct_semester(self.solution, grade_subject_1):
                        # swap
                        isMoveSubject = False
                        break
                    else:
                        available_subjects.remove(subject_pos_1)
                    # l.warn("Removing... show list")
                    # for available_subject in available_subjects:
                    #     l.info("%d) %s" % (available_subject ,extract_grade_subject(self.solution.semesters[semester_id_1].subjects[available_subject])))

                if isMoveSubject:
                    l.info("Preparing to move subect " + extract_grade_subject(grade_subject_0))
                    if len(available_semesters) > 0:
                        self.move_grade_subject(grade_subject_0, semester_id_1)
                    else:
                        l.warn("Can't find suitable semester for " + extract_grade_subject(grade_subject_0))
                else:
                    l.info("Swapping.. "+extract_grade_subject(grade_subject_0) + " with")
                    l.info("Swapping.. "+extract_grade_subject(grade_subject_1) )
                    self.swap_grade_subject(grade_subject_0, grade_subject_1)
        else:
            # l.warn("Preparing to move subject " + extract_grade_subject(grade_subject_0))
            l.warn("can't find available_semesters for " + extract_grade_subject(grade_subject_0))
            return None
        # self.spread_out_subject()
        return self.solution

    # def spread_out_subject(self):

        # average_credit = self.__find_average_credit(self.solution.member.num_studied_semester_id, len(self.solution.semesters))
        # l.info(average_credit)
        # # todo: Can do faster
        # # available_semesters = self.__find_available_semesters()
        # semester_id_0 = self.__find_max_credit_of_semester_id(self.solution.member.num_studied_semester_id, len(self.solution.semesters))
        # available_subjects = self.__get_available_subjects(semester_id_0)
        # if len(available_subjects) == 0:
        #     l.error("sth error")
        #     return None
        # subject_pos_0 = available_subjects[self.random_operator.randint(0, len(available_subjects) - 1)]
        # grade_subject_0 = self.solution.semesters[semester_id_0].subjects[subject_pos_0]
        # l.info(extract_grade_subject(grade_subject_0))
        # available_semesters = self.__get_low_credit_semester_ids(semester_id_0, average_credit)
        # if len(available_semesters) == 0:
        #     l.warn("Do not have low credit semester")
        #     return None
        #
        # semester_id_1 = self.__random_semester_id(available_semesters)
        # if semester_id_1 < 0:
        #     return None
        #
        # self.move_grade_subject(grade_subject_0, semester_id_1)
        # return self.solution


    def __get_low_credit_semester_ids(self, semester_id_0, average_credit):
        semester_ids = []
        for semester_id in range(self.solution.member.num_studied_semester_id, len(self.solution.semesters)):
            if semester_id == semester_id_0:
                continue
            if self.solution.semesters[semester_id].total_credit < average_credit:
                semester_ids.append(semester_id)
        return semester_ids

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

    def __random_semester_id(self, external_available_semesters=None):
        available_semesters = self.__find_not_empty_semester_ids(external_available_semesters)
        if len(available_semesters) == 0:
            return -1

        return available_semesters[self.random_operator.randint(0, len(available_semesters)-1)]

    def __find_not_empty_semester_ids(self, external_available_semesters=None):
        available_semesters = []
        if external_available_semesters is None:
            for semester_id in range(self.solution.member.num_studied_semester_id,
                                     len(self.solution.semesters)):
                if len(self.solution.semesters[semester_id].subjects) != 0:
                    available_semesters.append(semester_id)
        else:
            available_semesters = external_available_semesters
            # for semester_id in external_available_semesters:
            #     # if semester_id < len(self.solution.semesters):
            #     if len(self.solution.semesters[semester_id].subjects) != 0:
            #         available_semesters.append(semester_id)
        return available_semesters

    def __get_available_subjects(self, semester_id, grade_subject=None):
        available_subject_ids = []
        # available_subjects = copy.copy(self.solution.semesters[semester_id].subjects)
        # for grade_subject in available_subjects:
        #     if len(grade_subject.subject.reverse_prerequisites) > 0:
        #         available_subjects.remove(grade_subject)
        if semester_id < len(self.solution.semesters):
            semester = self.solution.semesters[semester_id]
            if grade_subject is None:
                for subject_id in range(len(semester.subjects)):
                    if len(semester.subjects[subject_id].subject.reverse_prerequisites) == 0:
                        available_subject_ids.append(subject_id)
            else:
                # Not in used
                for subject_id in range(len(semester.subjects)):
                    if grade_subject.subject.isSpecific is False and \
                            semester.subjects[subject_id].subject.isSpecific is True:
                        continue
                    if len(semester.subjects[subject_id].subject.reverse_prerequisites) == 0:
                        available_subject_ids.append(subject_id)
        return available_subject_ids