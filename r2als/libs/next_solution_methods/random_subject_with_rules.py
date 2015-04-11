from r2als.libs.functions import extract_grade_subject

__author__ = 'mildronize'

from r2als.libs.logs import Log
from r2als.libs.functions import *
from r2als import config
import copy
import os
from r2als.libs.rules import Rule
from r2als.libs.next_solution_methods import *
from r2als.libs.available_semesters import get_available_semesters
from r2als.libs.validators.grade_subject_in_curriculum import is_correct_semester

l = Log('nsm.random_subject_with_rules').getLogger()

class RandomSubjectWithRules(NextSolutionMethod):

    def get_solution(self, random_operator):
        self.rule = Rule(self.solution.member)
        self.random_operator = random_operator
        isMoveSubject = True
        # 1 random a semester_id(A) /
        # 2 random a subject(A) in semester_id(A)
        #       3. get_available_subjects (must not same semester and can swap)
        #       4. random semester(B) in get_available_semesters()
        #       5. random a subject(B) in condition following
        #             if the subject(B) can be enrolled in semester_id(A)
        #                   SWAPPING (Try to swap, if not move it)
        #             else  MOVING

        # 1
        semester_id_0 = self.__random_semester_id()
        # 2
        available_subjects = self.__get_available_subjects(semester_id_0)
        if len(available_subjects) == 0:
            l.error("Can't find available subjects for %d/%d: No have non-related subject" % ( self.si.toYear(semester_id_0), self.si.toSemester(semester_id_0)))
            # for semester_id in range(self.solution.member.num_studied_semester_id, len(self.solution.semesters)):
            #     l.warn("-> %d/%d (%d)"% ( self.si.toYear(semester_id), self.si.toSemester(semester_id), self.solution.semesters[semester_id].calculate_total_credit() ))
            return None
        subject_pos_0 = available_subjects[self.random_operator.randint(0, len(available_subjects) - 1)]
        grade_subject_0 = self.solution.semesters[semester_id_0].subjects[subject_pos_0]
        l.debug("grade_subject_0 >> " + extract_grade_subject(grade_subject_0))

        # 2.5
        # consider if chosen subject has
        # todo:

        # 3
        # available_semesters = get_available_semesters(self.solution, grade_subject_0, ignore_credit=False)

        if grade_subject_0.subject.not_fix_semester:
            # To move a subject
            available_subjects = []
        else:
            # To swap 2 subjects
            available_subjects = self._get_another_semester_subjects(grade_subject_0)
        # 4

        if len(available_subjects) > 0:
            # l.info("len(available_semesters) = " + str(len(available_semesters)))

            subject_pos_1 = self._random_subject_pos(available_subjects)
            if subject_pos_1 is not None:
                # 5
                grade_subject_1 = self.solution.semesters[subject_pos_1['semester_id']].subjects[subject_pos_1['subject_pos']]
                l.info("Swapping.. "+extract_grade_subject(grade_subject_0) + " with")
                l.info("Swapping.. "+extract_grade_subject(grade_subject_1) )
                self.swap_grade_subject(grade_subject_0, grade_subject_1)

                if 'english' in grade_subject_0.subject.tags:
                    l.warn("("+"-"*40)
                    l.warn("1: English is Swapped to %d/%d "% ( grade_subject_1.year, grade_subject_1.semester) )
                if 'english' in grade_subject_1.subject.tags:
                    l.warn("2: English is Swapped to %d/%d "% ( grade_subject_0.year, grade_subject_0.semester) )
                    l.warn(")"+"-"*40)
                return self.solution
            else:
                l.warn("Can't find target semester to move or swap "+ extract_grade_subject(grade_subject_0))
                return None

        l.info("Preparing to move subect " + extract_grade_subject(grade_subject_0))
        available_semesters = get_available_semesters(self.solution, grade_subject_0)
        semester_id_1 = self.__random_semester_id(available_semesters)

        if semester_id_1 >= 0:
            if len(available_semesters) > 0:
                self.move_grade_subject(grade_subject_0, semester_id_1)
                if 'english' in grade_subject_0.subject.tags:
                    l.warn("English is moved to %d/%d "% ( self.si.toYear(semester_id_1), self.si.toSemester(semester_id_1)) )
                return self.solution
            else:
                l.warn("Can't find suitable semester for " + extract_grade_subject(grade_subject_0))
                return None
        else:
            l.warn("Can't find target semester to move "+ extract_grade_subject(grade_subject_0))
            return None

        # l.warn("Preparing to move subject " + extract_grade_subject(grade_subject_0))
        l.warn("can't find available_subjects for " + extract_grade_subject(grade_subject_0))
        # l.warn("%d/%d (%d)"% ( self.si.toYear(semester_id_0), self.si.toSemester(semester_id_0), self.solution.semesters[semester_id_0].calculate_total_credit() ))
        # for semester_id in range(self.solution.member.num_studied_semester_id, len(self.solution.semesters)):
        #     if grade_subject_0.semester != self.si.toSemester(semester_id):
        #             #and  grade_subject.subject.isSpecific is True:
        #         continue`
        #     l.warn("-> %d/%d (%d)"% ( self.si.toYear(semester_id), self.si.toSemester(semester_id), self.solution.semesters[semester_id].calculate_total_credit() ))
        return None
        # self.spread_out_subject()


    def get_solution_tmp(self, random_operator):

        is_add_extra_semester = False
        self.random_operator = random_operator
        isMoveSubject = True
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
        if len(available_subjects) == 0:
            l.error("sth error")
            return None
        subject_pos_0 = available_subjects[self.random_operator.randint(0, len(available_subjects) - 1)]
        grade_subject_0 = self.solution.semesters[semester_id_0].subjects[subject_pos_0]
        l.debug("grade_subject_0 >> " + extract_grade_subject(grade_subject_0))

        # 2.5
        # consider if chosen subject has
        # todo:

        # 3
        available_semesters = get_available_semesters(self.solution, grade_subject_0, ignore_credit=False)
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

        # semester_id_1 = 0
        if len(available_semesters) > 0:
            # l.info("len(available_semesters) = " + str(len(available_semesters)))

            semester_id_1 = self.__random_semester_id(available_semesters)
            if semester_id_1 >= 0:
                # 5
                available_subjects = self.__get_available_subjects(semester_id_1)
                l.info("available_subjects of "+extract_grade_subject(grade_subject_0))
                for available_subject in available_subjects:
                    l.debug("%d) %s" % (available_subject, extract_grade_subject(self.solution.semesters[semester_id_1].subjects[available_subject])))
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
                    available_semesters = get_available_semesters(self.solution, grade_subject_0)
                    semester_id_1 = self.__random_semester_id(available_semesters)
                    if semester_id_1 >= 0:
                        if len(available_semesters) > 0:
                            self.move_grade_subject(grade_subject_0, semester_id_1)
                        else:
                            l.warn("Can't find suitable semester for " + extract_grade_subject(grade_subject_0))
                            return None
                    else:
                        l.warn("Can't find target semester to move "+ extract_grade_subject(grade_subject_0))
                        return None
                else:
                    l.info("Swapping.. "+extract_grade_subject(grade_subject_0) + " with")
                    l.info("Swapping.. "+extract_grade_subject(grade_subject_1) )
                    self.swap_grade_subject(grade_subject_0, grade_subject_1)
            else:
                l.warn("Can't find target semester to move or swap "+ extract_grade_subject(grade_subject_0))
                return None
        else:
            # l.warn("Preparing to move subject " + extract_grade_subject(grade_subject_0))
            l.warn("can't find available_semesters for " + extract_grade_subject(grade_subject_0))
            l.warn("%d/%d (%d)"% ( self.si.toYear(semester_id_0), self.si.toSemester(semester_id_0), self.solution.semesters[semester_id_0].calculate_total_credit() ))
            for semester_id in range(self.solution.member.num_studied_semester_id, len(self.solution.semesters)):
                if grade_subject_0.semester != self.si.toSemester(semester_id):
                        #and  grade_subject.subject.isSpecific is True:
                    continue
                l.warn("-> %d/%d (%d)"% ( self.si.toYear(semester_id), self.si.toSemester(semester_id), self.solution.semesters[semester_id].calculate_total_credit() ))
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

    def _get_another_semester_subjects(self, grade_subject):
        tmp = []
        cur_semester_id = self.si.get(grade_subject.year, grade_subject.semester)

        for semester_id in range(self.solution.member.num_studied_semester_id, len(self.solution.semesters)):
            if semester_id == cur_semester_id:
                continue
            # if grade_subject.semester != self.si.toSemester(semester_id):
            #     continue
            #
            # If subject is normal
            # if not grade_subject.subject.not_fix_semester:
            if grade_subject.semester != self.si.toSemester(semester_id):
                continue
            i = 0
            for t_grade_subject in self.solution.semesters[semester_id].subjects:
                if len(t_grade_subject.subject.reverse_prerequisites) != 0:
                    i+=1
                    continue
                if self.solution.semesters[cur_semester_id].calculate_total_credit() - \
                    grade_subject.subject.credit + \
                    t_grade_subject.subject.credit > \
                        self.rule.calculate_maximum_credit(cur_semester_id):
                    i+=1
                    # if debug:
                    #     l.warn("1) %s vs %s : %d-%d+%d > %d" % (extract_grade_subject(grade_subject),
                    #                                          extract_grade_subject(t_grade_subject),
                    #                                          self.solution.semesters[cur_semester_id].calculate_total_credit(),
                    #                                          grade_subject.subject.credit,
                    #                                          t_grade_subject.subject.credit,
                    #                                          self.rule.calculate_maximum_credit(cur_semester_id)))
                    continue
                if self.solution.semesters[semester_id].calculate_total_credit() + \
                    grade_subject.subject.credit - \
                    t_grade_subject.subject.credit > \
                        self.rule.calculate_maximum_credit(semester_id):
                    i+=1
                    # if debug:
                    #     l.warn("2) %s vs %s : %d+%d-%d > %d" % (extract_grade_subject(grade_subject),
                    #                                          extract_grade_subject(t_grade_subject),
                    #                                          self.solution.semesters[semester_id].calculate_total_credit(),
                    #                                          grade_subject.subject.credit,
                    #                                          t_grade_subject.subject.credit,
                    #                                          self.rule.calculate_maximum_credit(semester_id)))
                    continue
                tmp.append({'semester_id':semester_id,'subject_pos':i})
                i+=1
        return tmp

    def _random_subject_pos(self, available_subjects):
        if len(available_subjects) == 0:
            return None
        return available_subjects[self.random_operator.randint(0, len(available_subjects)-1)]

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
                if len(self.solution.semesters[semester_id].subjects) != 0 and \
                        len(self.__get_available_subjects(semester_id)) != 0:
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

        if semester_id < len(self.solution.semesters):
            semester = self.solution.semesters[semester_id]
            if grade_subject is None:
                for subject_id in range(len(semester.subjects)):
                    if len(semester.subjects[subject_id].subject.reverse_prerequisites) == 0:
                        available_subject_ids.append(subject_id)
            # Not use now
            # else:
            #
            #     for subject_id in range(len(semester.subjects)):
            #         if grade_subject.subject.isSpecific is False and \
            #                 semester.subjects[subject_id].subject.isSpecific is True:
            #             continue
            #         if len(semester.subjects[subject_id].subject.reverse_prerequisites) == 0:
            #             available_subject_ids.append(subject_id)
        return available_subject_ids

    def __get_all_subjects(self, semester_id):
        available_subject_ids = []
        if semester_id < len(self.solution.semesters):
            semester = self.solution.semesters[semester_id]
            for subject_id in range(len(semester.subjects)):
                available_subject_ids.append(subject_id)
        return available_subject_ids