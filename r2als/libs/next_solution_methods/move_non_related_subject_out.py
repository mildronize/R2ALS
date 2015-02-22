__author__ = 'mildronize'

from random import randint
from r2als.libs.rules import Rule
from r2als.libs.logs import Log
from r2als.libs.next_solution_methods import *
from r2als.libs.available_semesters import get_available_semesters
l = Log('nsm.move_non_related_subject_out').getLogger()

# todo: This class is not good because must use self.solution.get_ready() for fix sth

class MoveNonRelatedSubjectOut(NextSolutionMethod):

    def get_solution(self):
        self.move_non_related_subject_out()
        return self.solution

    def move_non_related_subject_out(self):
        # 1 get all non_related subject
        # last semester of the member

        self.rule = Rule(self.solution.member)
        last_semester_id = self.si.get(self.solution.member.last_year,
                                       self.solution.member.last_semester)

        for i in range(last_semester_id+1, len(self.solution.semesters)):
            maximum_credit = self.rule.calculate_maximum_credit(i)
            total_credit = self.solution.semesters[i].calculate_total_credit()
            if total_credit > maximum_credit:
                over_credit = total_credit - maximum_credit
                l.info("Over %d credits in semester: %d/%d" % (over_credit,
                                                               self.si.toYear(i),
                                                               self.si.toSemester(i)))

                temp_subjects = []
                # To find non related subject
                non_related_grade_subjects = self.solution.semesters[i].find_non_related_subjects()

                while over_credit > 0:
                    random_position = randint(0,len(non_related_grade_subjects) - 1)
                    over_credit -= non_related_grade_subjects[random_position].subject.credit
                    # remove the subject
                    l.info("over credit %d , removing > %s " % (over_credit,
                                                                non_related_grade_subjects[random_position].subject.short_name))
                    temp_subjects.append(non_related_grade_subjects[random_position])
                    self.solution.semesters[i].subjects.remove(non_related_grade_subjects[random_position])
                    non_related_grade_subjects.remove(non_related_grade_subjects[random_position])
                # find the semesters that allow the subject to move in the semester

                for temp_grade_subject in temp_subjects:
                    # available_semesters = self.get_available_semesters(i, temp_subject)
                    available_semesters = get_available_semesters(self.solution, temp_grade_subject)
                    random_semester = randint(0, len(available_semesters) - 1 )
                    self.solution.extend_semester_size(available_semesters[random_semester])
                    self.solution.semesters[available_semesters[random_semester]].subjects.append(temp_grade_subject)

                # print(self.solution.semesters[i].calculate_total_credit())

    # def get_available_semesters(self, index, temp_subject):
    #     # l.info("available_semester: %s (credit : %d)" % (temp_subject.subject.short_name, temp_subject.subject.credit))
    #     available_semesters = []
    #     semester = self.si.toSemester(index)
    #     for semester_id in range(self.solution.member.num_studied_semester_id, len(self.solution.semesters)):
    #         if semester != self.si.toSemester(semester_id):
    #             continue
    #         if semester_id == index:
    #             continue
    #         if self.solution.semesters[semester_id].calculate_total_credit() + temp_subject.subject.credit > self.rule.calculate_maximum_credit(semester_id):
    #             continue
    #         available_semesters.append(semester_id)
    #     # for semester_id,mSemester in enumerate(self.solution.semesters):
    #     #     if semester == self.si.toSemester(semester_id) and \
    #     #        semester_id != index and \
    #     #        mSemester.calculate_total_credit() + temp_subject.subject.credit <= self.rule.calculate_maximum_credit(semester_id):
    #     #         available_semesters.append(semester_id)
    #     return available_semesters
    #     # l.info("%d/%d" % (self.si.toYear(semester_id), self.si.toSemester(semester_id)))
