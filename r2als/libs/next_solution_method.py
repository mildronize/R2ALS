__author__ = 'mildronize'

import abc

from r2als.libs.logs import Log
from r2als.libs.functions import *
l = Log('next_solution_method').getLogger()

class NextSolutionMethod(object):

    __metaclass__ = abc.ABCMeta

    def __init__(self, solution):
        self.solution = solution
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
        tmp = self.solution.semesters[semester_id_1].subjects.pop(target_subject_1_position)
        self.solution.semesters[semester_id_2].subjects.append(tmp)

        self.solution.semesters[semester_id_1].subjects.append(
            self.solution.semesters[semester_id_2].subjects.pop(target_subject_2_position)
        )
        # swapping year & semester
        grade_subject_1.year, grade_subject_2.year = grade_subject_2.year, grade_subject_1.year
        grade_subject_1.semester, grade_subject_2.semester = grade_subject_2.semester, grade_subject_1.semester

        l.info("Swapping %s & %s" % (extract_grade_subject(grade_subject_1), extract_grade_subject(grade_subject_2)))

    def move_grade_subject(self, grade_subject, target_semester_id):
        # Prepare var
        msg = "Can't move subject into "+ str(self.si.toYear(target_semester_id))+"/"+str(self.si.toSemester(target_semester_id) ) +" because: "

        semester_id = self.si.get(grade_subject.year, grade_subject.semester)
        subject_position = self.__find_grade_subject_id(semester_id, grade_subject.subject)
        if subject_position >= 0:
            # extending the semester
            self.solution.extend_semester_size(target_semester_id)
            # Moving
            l.info("Moving subject %s to %d/%d" % (extract_grade_subject(grade_subject), self.si.toYear(target_semester_id), self.si.toSemester(target_semester_id) ) )
            self.solution.semesters[target_semester_id].subjects.append(
                self.solution.semesters[semester_id].subjects.pop(subject_position)
            )

            grade_subject.year = self.si.toYear(target_semester_id)
            grade_subject.semester = self.si.toSemester(target_semester_id)
        elif subject_position == -1:
            l.error(msg + "Can't find gradesubject " + extract_grade_subject(grade_subject))
        elif subject_position == -2:
            l.error(msg + extract_grade_subject(grade_subject)+ " is a fail subject ( studied subject)")

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
        if semester_id < self.solution.member.num_studied_semester_id:
            return -2
        for i in range(len(self.solution.semesters[semester_id].subjects)):
            tmp_subject = self.solution.semesters[semester_id].subjects[i].subject
            if subject == tmp_subject:
                return i
        return -1
