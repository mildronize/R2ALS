__author__ = 'mildronize'


from r2als.libs.rules import Rule
from r2als import config
from r2als.libs.logs import Log
from r2als.libs.next_solution_methods import *
from r2als.libs.available_semesters import get_available_semesters
l = Log('nsm.move_non_related_subject_out').getLogger()

# todo: This class is not good because must use self.solution.get_ready() for fix sth

class MoveSubjectOut(NextSolutionMethod):

    def get_solution(self, random_operator):
        l.info("Move Non Related Subject Out start")
        self.random_operator = random_operator
        if self.move_non_related_subject_out() is False:
            # no non_related_grade_subjects try to move related subject out instead
            self.move_related_subject_out()
        return self.solution

    def select_related_subject(self, semester_id):
        # random selected
        subject_pos = self.random_operator.randint(0,
                                                   len(self.solution.semesters[semester_id].subjects))
        return self.solution.semesters[semester_id].subjects[subject_pos]

    def move_related_subject_out(self):
        print("555")
        self.rule = Rule(self.solution.member)
        for semester_id in range(self.solution.member.num_studied_semester_id, len(self.solution.semesters)):
            maximum_credit = self.rule.calculate_maximum_credit(semester_id)
            while self.solution.semesters[semester_id].calculate_total_credit() <= maximum_credit:
                selected_subject = self.select_related_subject(semester_id)
                target_semester_id = self.si.get(selected_subject.year+1, selected_subject.semester)
                self.move_grade_subject(selected_subject, target_semester_id)
                self.solution = MoveWholeChain(self.solution).get_solution()


    def move_non_related_subject_out(self):
        # 1 get all non_related subject
        # last semester of the member
        # random.seed(config.random_seed)

        self.rule = Rule(self.solution.member)
        # last_semester_id = self.si.get(self.solution.member.last_year,
        #                                self.solution.member.last_semester)

        for i in range(self.solution.member.num_studied_semester_id, len(self.solution.semesters)):
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

                if len(non_related_grade_subjects) == 0:
                    l.warn("Error, no non_related_grade_subjects try to move related subject out instead")
                    return False

                while over_credit > 0:
                    random_position = self.random_operator.randint(0,len(non_related_grade_subjects) - 1)
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
                    if len(available_semesters) > 0:
                        random_semester = self.random_operator.randint(0, len(available_semesters) - 1 )
                        self.solution.extend_semester_size(available_semesters[random_semester])
                        self.solution.semesters[available_semesters[random_semester]].subjects.append(temp_grade_subject)

                # print(self.solution.semesters[i].calculate_total_credit())
        return True