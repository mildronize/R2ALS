__author__ = 'mildronize'

import abc

from r2als.libs.logs import Log
from r2als.libs.functions import *
l = Log('next_solution_method').getLogger()

class NextSolutionMethod(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, solution):
        self.solution = solution
        # self.mSemesters = solution.semesters
        # self.member = solution.member
        self.si = SemesterIndex(solution.member.curriculum.num_semester)

    @abc.abstractmethod
    def get_solution(self):
        """Retrieve solution"""
        return

    def swap_grade_subject(self, grade_subject_1, grade_subject_2):
        # Prepare var
        si = SemesterIndex(self.solution.member.curriculum.num_semester)
        semester_id_1 = si.get(grade_subject_1.year, grade_subject_1.semester)
        target_subject_1_position = self.__find_grade_subject_id(semester_id_1,
                                                                 grade_subject_1.subject)
        if target_subject_1_position < 0:
            l.error("not found subject")

        semester_id_2 = si.get(grade_subject_2.year, grade_subject_2.semester)
        target_subject_2_position = self.__find_grade_subject_id(semester_id_2,
                                                                 grade_subject_2.subject)

        if target_subject_2_position < 0:
            l.error("not found subject")
        # Swapping
        l.info("Before Swapping %s & %s" % (extract_grade_subject(grade_subject_1), extract_grade_subject(grade_subject_2)))
        l.info("Before "+extract_solution(self.solution, semester_id_1))
        l.info("Before "+extract_solution(self.solution, semester_id_2))
        # l.info("Before "+extract_solution(self.solution, semester_id_1))
        tmp = self.solution.semesters[semester_id_1].subjects.pop(target_subject_1_position)
        # l.info("Removing "+extract_grade_subject(tmp))
        # l.info("After "+extract_solution(self.solution, semester_id_1))

        # l.info("*"*45)

        # l.info("Before "+extract_solution(self.solution, semester_id_2))
        self.solution.semesters[semester_id_2].subjects.append(tmp)
        # l.info("Adding "+extract_grade_subject(tmp))
        # l.info("After "+extract_solution(self.solution, semester_id_2))

        # l.info("*"*45)

        # l.info("Before "+extract_solution(self.solution, semester_id_2))
        # tmp = self.solution.semesters[semester_id_2].subjects.pop(target_subject_2_position)
        # l.info("Removing "+extract_grade_subject(tmp))
        # l.info("After "+extract_solution(self.solution, semester_id_2))

        # l.info("*"*45)

        self.solution.semesters[semester_id_1].subjects.append(
            self.solution.semesters[semester_id_2].subjects.pop(target_subject_2_position)
        )
        # swapping year & semester
        grade_subject_1.year, grade_subject_2.year = grade_subject_2.year, grade_subject_1.year
        grade_subject_1.semester, grade_subject_2.semester = grade_subject_2.semester, grade_subject_1.semester
        l.info("After "+extract_solution(self.solution, semester_id_1))
        l.info("After "+extract_solution(self.solution, semester_id_2))
        l.info("After Swapping %s & %s" % (extract_grade_subject(grade_subject_1), extract_grade_subject(grade_subject_2)))


    def moveGradeSubject(self, source_semester, source_subject_order, target_semester):
        l.warn("This function is deprecated, please use \"move_grade_subject\" instead")
        msg = 'Moving "%s"\t(%d/%d) to (%d/%d)' % ( self.solution.semesters[source_semester].subjects[source_subject_order].subject.short_name,
                                                self.si.toYear(source_semester),
                                                self.si.toSemester(source_semester),
                                                self.si.toYear(target_semester),
                                                self.si.toSemester(target_semester))
        if source_semester == target_semester:
            l.error(msg)
        else:
            l.info(msg)

            # tmp_gradeSubject = copy.copy(self.mSemesters[source_semester].subjects[source_subject_order])
            # move
            # self.mSemesters[target_semester].subjects.append(self.mSemesters[source_semester].subjects[source_subject_order])
            # # remove
            # self.mSemesters[source_semester].subjects.pop(source_subject_order)
            self.solution.semesters[target_semester].subjects.append(
                self.solution.semesters[source_semester].subjects.pop(source_subject_order)
            )

    def __find_grade_subject_id(self, semester_id, subject):
        for i in range(len(self.solution.semesters[semester_id].subjects)):
            tmp_subject = self.solution.semesters[semester_id].subjects[i].subject
            if subject == tmp_subject:
                return i
        return -1
