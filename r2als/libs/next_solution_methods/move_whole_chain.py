__author__ = 'mildronize'

from random import randint
from r2als import models
from r2als.libs.logs import Log
from r2als.libs import prerequisites
from r2als.libs.next_solution_method import NextSolutionMethod
from r2als.libs.rules import Rule
from r2als.libs.subject_list import SubjectList

l = Log('move_whole_chain').getLogger()

class MoveWholeChain(NextSolutionMethod):


    def move_non_related_subject_out(self):
        # 1 get all non_related subject
        # last semester of the member


        non_related_grade_subjects = []
        rule = Rule(self.member)
        last_semester_id = self.si.get(self.member.last_year,
                                       self.member.last_semester)

        for i in range(last_semester_id+1, len(self.mSemesters)):
            maximum_credit = rule.calculate_maximum_credit(i)
            total_credit = self.mSemesters[i].calculate_total_credit()
            if total_credit > maximum_credit:
                over_credit = total_credit - maximum_credit
                l.error("Over %d credits in semester: %d/%d" % (over_credit,
                                                                self.si.toYear(i),
                                                                self.si.toSemester(i)))
                # To find non related subject
                for gradeSubject in self.mSemesters[i].subjects:
                    if gradeSubject.subject.prerequisites == [] and \
                    gradeSubject.subject.reverse_prerequisites == []:
                        # add subject into subject_list
                        non_related_grade_subjects.append(gradeSubject)
                        l.info("%s (%d)" % (gradeSubject.subject.short_name,
                                            gradeSubject.subject.credit))

                while over_credit > 0:
                    random_position = randint(0,len(non_related_grade_subjects) - 1)
                    over_credit -= non_related_grade_subjects[random_position].subject.credit
                    # remove the subject
                    l.info("over credit %d , removing > %s " % (over_credit,
                                                                non_related_grade_subjects[random_position].subject.short_name))
                    self.mSemesters[i].subjects.remove(non_related_grade_subjects[random_position])
                    non_related_grade_subjects.remove(non_related_grade_subjects[random_position])
                print(self.mSemesters[i].calculate_total_credit())
        return None

    def find_fail_subjects(self):
        # interest only studied semester
        result_list = []
        last_semester_id = self.si.get(self.member.last_year, self.member.last_semester) + 1
        for i in range(last_semester_id):
            for gradeSubject in self.mSemesters[i].subjects:
                if gradeSubject.grade.mustReEnroll:
                    result_list.append(models.GradeSubject(subject = gradeSubject.subject,
                                                            year = self.si.toYear(i),
                                                            semester = self.si.toSemester(i),
                                                            grade = gradeSubject.grade))
        return result_list

    def find_subject(self, failSubject):
        last_semester_id = self.si.get(self.member.last_year, self.member.last_semester) + 1
        for i in range(last_semester_id, len(self.mSemesters)):
            # l.info('processing %s',i)
            for subject_order, subject_obj in enumerate(self.mSemesters[i].subjects):
                if failSubject == subject_obj.subject:
                    return {
                        'semester_id': i,
                        'subject_order': subject_order
                    }
        return None

    def get_target_semester(self, previous_gradeSubject, subject ,last_year, last_semester, source_iden, prerequisite_name):
        target_semester = dict()
        last_semester_id = self.si.get(last_year, last_semester) + 1
        subjectGroup = models.SubjectGroup.objects(subject_id = subject.id,
                                                   name = self.member.subject_group).first()
        if subjectGroup is None:
            return -1
        original_semester_id = self.si.get(subjectGroup.year,
                                  subjectGroup.semester)
        source_year = self.si.toYear(source_iden['semester_id'])
        source_semester = self.si.toSemester(source_iden['semester_id'])
        if original_semester_id < last_semester_id:
            # move to next year and same semester
            target_semester['year'] = last_year + 1
            target_semester['semester'] = subjectGroup.semester
        else:
            # move to next year and same semester from previous subject
            if prerequisite_name is None:
                l.error('Must have prerequisite_name')
                return -2

            target_semester['year'] = previous_gradeSubject.year # + 1
            target_semester['semester'] = subjectGroup.semester
            check = True
            while check:
                target_gradeSubject = models.GradeSubject(subject = subject,
                                                           year = target_semester['year'],
                                                           semester = target_semester['semester'])
                p = prerequisites.selector(prerequisite_name, previous_gradeSubject, target_gradeSubject, self.member)
                if p.canEnrolled() == True:
                    check = False
                else:
                    target_semester['year'] += 1
                if target_semester['year'] > self.member.curriculum.required_num_year + 1:
                    # check = False
                    l.error('Can\'t find suitable semester id for %s', subject.name)
                    return -3

        return self.si.get(target_semester['year'], target_semester['semester'])

    def prepare_moving(self, previous_gradeSubject, gradeSubject, prerequisite_name):
        if previous_gradeSubject is None:
            l.debug("START >> %s", gradeSubject.subject.short_name)
        else:
            l.debug("%s (%s/%s) >> %s", previous_gradeSubject.subject.short_name,
                                        previous_gradeSubject.year,
                                        previous_gradeSubject.semester,
                                        gradeSubject.subject.short_name)
        source_iden = self.find_subject(gradeSubject.subject)
        if source_iden is not None:
            target_semester = self.get_target_semester(previous_gradeSubject,
                                                     gradeSubject.subject,
                                                     self.member.last_year,
                                                     self.member.last_semester,
                                                     source_iden,
                                                     prerequisite_name)
            if target_semester < 0:
                l.error('Impossible enroll of %s', gradeSubject.subject.name)
            else :
                self.moveGradeSubject(source_iden['semester_id'],
                                      source_iden['subject_order'],
                                      target_semester)
        else:
            l.error('Not found subject %s', gradeSubject.subject.name)

    def move_subject_whole_chain(self, previous_gradeSubject, gradeSubject):
        # l.info("Create new runSameChain : %s", subject.short_name)
        subject = gradeSubject.subject
        if previous_gradeSubject is None:
            self.prepare_moving(None, gradeSubject, None)
        if subject.reverse_prerequisites is []:
            return 0
        else:
            for reverse_prerequisite in subject.reverse_prerequisites:
                semester_id = self.find_subject(subject)['semester_id']
                tmp_gradeSubject = models.GradeSubject(subject = subject,
                                                       year = self.si.toYear(semester_id),
                                                       semester = self.si.toSemester(semester_id),
                                                       )
                prerequisite_gradeSubject = models.GradeSubject(subject = reverse_prerequisite.subject)
                self.prepare_moving(tmp_gradeSubject, prerequisite_gradeSubject, reverse_prerequisite.name)
                self.move_subject_whole_chain(tmp_gradeSubject, prerequisite_gradeSubject)

    def start(self):
        # step 1 : find fail subject
        # step 2 : store it in list
        fail_subject = self.find_fail_subjects()
        # for gradeSubject in fail_subject:
        #     l.info(gradeSubject.subject.short_name)
        # step 3 : move back each semester
        # Loop in remaining semester

        # last_semester_id = self.si.get(self.member.last_year, self.member.last_semester) + 1
        for failGradeSubject in fail_subject:
            self.move_subject_whole_chain(None, failGradeSubject)

        # find fail_subject
        #   In each loop: swap the fail subject to nearest semester
        #
        self.move_non_related_subject_out()

        return self.mSemesters

    # simple getTargetSemester
    # def getTargetSemester(self, previous_gradeSubject, subject ,last_year, last_semester, source_iden):
    #     last_semester_id = self.si.get(last_year, last_semester) + 1
    #     subjectGroup = models.SubjectGroup.objects(subject_id = subject.id,
    #                                                name = self.member.subject_group).first()
    #     if subjectGroup is None:
    #         return -1
    #     semester_id = self.si.get(subjectGroup.year,
    #                               subjectGroup.semester)
    #     source_year = self.si.toYear(source_iden['semester_id'])
    #     source_semester = self.si.toSemester(source_iden['semester_id'])
    #     if semester_id < last_semester_id:
    #         # move to next year and same semester
    #         return self.si.get(last_year + 1, subjectGroup.semester)
    #     else :
    #         # move to next year and same semester from previous subject
    #         return self.si.get(previous_gradeSubject.year + 1, subjectGroup.semester)
