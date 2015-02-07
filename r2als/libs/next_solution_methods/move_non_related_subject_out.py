__author__ = 'mildronize'

from random import randint
from r2als.libs.rules import Rule
from r2als.libs.logs import Log
from r2als.libs.next_solution_methods import *
l = Log('move_non_related_subject_out').getLogger()

class MoveNonRelatedSubjectOut(NextSolutionMethod):

    def get_solution(self):
        self.move_non_related_subject_out()
        return self.solution

    def move_non_related_subject_out(self):
        # 1 get all non_related subject
        # last semester of the member

        rule = Rule(self.solution.member)
        last_semester_id = self.si.get(self.solution.member.last_year,
                                       self.solution.member.last_semester)

        for i in range(last_semester_id+1, len(self.solution.semesters)):
            maximum_credit = rule.calculate_maximum_credit(i)
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
                semester = self.si.toSemester(i)
                # year = self.si.toYear(i)
                for temp_subject in temp_subjects:
                    available_semesters = []
                    l.info("available_semester: %s (credit : %d)" % (temp_subject.subject.short_name, temp_subject.subject.credit))
                    for key,mSemester in enumerate(self.solution.semesters):
                        if semester == self.si.toSemester(key) and key != i and \
                        mSemester.calculate_total_credit() + temp_subject.subject.credit <= rule.calculate_maximum_credit(key):
                            available_semesters.append(key)
                            l.info("%d/%d" % (self.si.toYear(key), self.si.toSemester(key)))
                    random_semester = randint(0, len(available_semesters) - 1 )
                    self.solution.semesters[available_semesters[random_semester]].subjects.append(temp_subject)

                # print(self.solution.semesters[i].calculate_total_credit())