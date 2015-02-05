__author__ = 'mildronize'
import copy
from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex
l = Log('next_solution_method').getLogger()

class NextSolutionMethod:

    def __init__(self, solution):
        self.mSemesters = solution.semesters
        self.member = solution.member
        self.si = SemesterIndex(self.member.curriculum.num_semester)

    def swap_gradeSubject(self, gs1, gs2):
        l.info('Swap sth')

    def moveGradeSubject(self, source_semester, source_subject_order, target_semester):
        l.warn("This function is deprecated, please use \"Solution.move_grade_subject\" instead")
        msg = 'Moving "%s"\t(%d/%d) to (%d/%d)' % ( self.mSemesters[source_semester].subjects[source_subject_order].subject.short_name,
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
            self.mSemesters[target_semester].subjects.append(
                self.mSemesters[source_semester].subjects.pop(source_subject_order)
            )
            
