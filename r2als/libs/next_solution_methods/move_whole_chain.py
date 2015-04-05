__author__ = 'mildronize'

# from random import randint
from r2als import models
from r2als.libs.logs import Log
from r2als.libs import prerequisites
from r2als.libs.next_solution_methods import *
from r2als.libs.functions import *
from r2als.libs.validators import prerequisite_check

l = Log('nsm.move_whole_chain').getLogger()

class MoveWholeChain(NextSolutionMethod):

    def get_solution(self):
        l.info("Move Whole Chain start")
        invalid_grade_subjects = prerequisite_check(solution=self.solution,
                                                    quick_checking=False,
                                                    isReversed=False)

        for invalid_grade_subject in invalid_grade_subjects:
            # l.info(extract_grade_subject(invalid_grade_subject))
            l.info(extract_grade_subject(invalid_grade_subject['grade_subject'])+"   "+extract_grade_subject(invalid_grade_subject['prerequisite_grade_subject']))
            self.move_subject_whole_chain(invalid_grade_subject['prerequisite_grade_subject'],
                                          invalid_grade_subject['grade_subject'],
                                          True)

        return self.solution

    def get_initial_solution(self, external_grade_subjects=None):
        l.info("get_initial_solution....")
         # step 1 : find fail subject
        if external_grade_subjects is None:
            subjects = self.find_fail_subjects()
        else:
            subjects = external_grade_subjects
        # step 3 : move back each semester
        # Loop in remaining semester
        for grade_subject in subjects:
            # l.warn(extract_grade_subject(fail_grade_subject))
            self.move_subject_whole_chain(grade_subject)
        return self.solution

    def move_subject_whole_chain(self, grade_subject, previous_grade_subject=None, has_previous=False):
        subject = grade_subject.subject
        if previous_grade_subject is None and has_previous is False:
            # fail subject
            self.move_subject(grade_subject)
        if subject.reverse_prerequisites is []:
            return 0
        else:
            for reverse_prerequisite in subject.reverse_prerequisites:
                semester_id = self.find_subject_in_not_studied_semester(subject)['semester_id']
                tmp_grade_subject = models.GradeSubject(subject = subject,
                                                        year = self.si.toYear(semester_id),
                                                        semester = self.si.toSemester(semester_id))
                # prerequisite_grade_subject = models.GradeSubject(subject = reverse_prerequisite.subject)
                # l.warn(extract_grade_subject(reverse_prerequisite.grade_subject))
                self.move_subject(grade_subject=reverse_prerequisite.grade_subject,
                                  previous_grade_subject=tmp_grade_subject,
                                  prerequisite_name=reverse_prerequisite.name,
                                  has_previous=has_previous)
                # def move_subject(self, previous_grade_subject, grade_subject, prerequisite_name, has_previous=False):
                self.move_subject_whole_chain(reverse_prerequisite.grade_subject, tmp_grade_subject, has_previous)

    def move_subject(self, grade_subject, previous_grade_subject=None, prerequisite_name=None, has_previous=False):
        # source_subject_pos = self.find_subject_in_not_studied_semester(grade_subject.subject)
        # if source_subject_pos is not None:
        if grade_subject.year is None or grade_subject.semester is None:
            source_subject_pos = self.find_subject_in_not_studied_semester(grade_subject.subject)['semester_id']
            grade_subject.year = self.si.toYear(source_subject_pos)
            grade_subject.semester = self.si.toSemester(source_subject_pos)

        # l.warn(extract_grade_subject(previous_grade_subject)+ " <-- " + extract_grade_subject(grade_subject))
        # if self.si.get(grade_subject.year, grade_subject.semester) >= self.solution.member.num_studied_semester_id:
        #     l.warn(extract_grade_subject(previous_grade_subject)+ " <-- " + extract_grade_subject(grade_subject))
        target_semester_id = self.get_target_semester(previous_grade_subject,
                                                       grade_subject,
                                                       prerequisite_name,
                                                       has_previous)
        # l.info("target_semester_id "+str(target_semester_id))
        if target_semester_id == -5:
            l.warn('Can\'t find suitable semester id for %s', grade_subject.subject.name)
        elif target_semester_id < 0:
            l.error('Impossible enroll of %s', grade_subject.subject.name)
        else:
            self.move_grade_subject(grade_subject, target_semester_id)

    def get_target_semester(self, previous_grade_subject, grade_subject, prerequisite_name, has_previous):

        target_semester = dict()
        subjectGroup = models.SubjectGroup.objects(subject_id=grade_subject.subject.id,
                                                   name=self.solution.member.subject_group).first()
        if subjectGroup is None:
            l.error("Not found the subject")
            return -1

        original_semester_id = self.si.get(subjectGroup.year, subjectGroup.semester)
        # Consider the studied subject in the studied semester_id
        if has_previous is False:
            # l.info("%d < %d" % (original_semester_id, self.solution.member.num_studied_semester_id))
            # if self.si.get(grade_subject.year, grade_subject.semester) >= self.solution.member.num_studied_semester_id:
            # l.warn(">> "+ extract_grade_subject(grade_subject)+ ": fail subject")
            if original_semester_id < self.solution.member.num_studied_semester_id:
                # This condition for fail subject only
                # move to next year and same semester
                target_semester['year'] = self.solution.member.last_year + 1
                target_semester['semester'] = subjectGroup.semester
                l.debug(">> "+ extract_grade_subject(grade_subject)+ ": fail subject")

            elif previous_grade_subject is None:
                l.error("previous_grade_subject is None")
                return -4
            else:
                l.debug(">> "+ extract_grade_subject(grade_subject)+ ": pass subject")
                # move to next year and same semester from previous subject
                # l.info(extract_grade_subject(previous_grade_subject))

                if prerequisite_name is None:
                    l.error('Must have prerequisite_name')
                    return -2
                # initial target_semester

                enrollable_semester = self.__find_enrollable_semester(year=previous_grade_subject.year,
                                                                    semester=subjectGroup.semester,
                                                                    previous_grade_subject=previous_grade_subject,
                                                                    grade_subject=grade_subject,
                                                                    prerequisite_name=prerequisite_name)
                if enrollable_semester is None:
                    return -3
                else:
                    target_semester['year'] = enrollable_semester['year']
                    target_semester['semester'] = enrollable_semester['semester']
        else:
            # l.info("has_previous is True")
            if previous_grade_subject is None:
                l.error("previous_grade_subject is None")
                return -2
            if prerequisite_name is None:
                l.error('Must have prerequisite_name')
                return -2
            # l.warn(extract_grade_subject(grade_subject))
            enrollable_semester = self.__find_enrollable_semester(year=grade_subject.year,
                                                                  semester=grade_subject.semester,
                                                                  previous_grade_subject=previous_grade_subject,
                                                                  grade_subject=grade_subject,
                                                                  prerequisite_name=prerequisite_name)
            if enrollable_semester is None:
                return -5
            else:
                target_semester['year'] = enrollable_semester['year']
                target_semester['semester'] = enrollable_semester['semester']

        return self.si.get(target_semester['year'], target_semester['semester'])

    def __find_enrollable_semester(self, year, semester, previous_grade_subject, grade_subject, prerequisite_name):
        # year = 0
        # semester = 0
        check = True
        while check:
            target_grade_subject = models.GradeSubject(subject = grade_subject.subject,
                                                       year = year,
                                                       semester = semester)
            # l.info("target_grade_subject: "+extract_grade_subject(target_grade_subject))
            # l.info(semester)
            p = prerequisites.selector(prerequisite_name, previous_grade_subject, target_grade_subject, self.solution.member)
            if p.canEnrolled() is True:
                check = False
            else:
                year += 1
            if year > self.solution.member.curriculum.max_year:
                # check = False
                # l.error('Can\'t find suitable semester id for %s', grade_subject.subject.name)
                return None

        return {
            'year': year,
            'semester': semester
        }


        #
        # if previous_grade_subject is None:
        #     # This condition for fail subject
        #     l.info("First time for recurring")
        #     # Check if the subject is fail
        #     if grade_subject.grade is not None:
        #         # Failed subject
        #         if grade_subject.grade.mustReEnroll:
        #             # Consider the studied subject in the studied semester_id
        #             if original_semester_id < self.solution.member.num_studied_semester_id:
        #                 # This condition for fail subject only
        #                 # Remark!!!!!!!
        #                 # move to next year and same semester
        #                 target_semester['year'] = self.solution.member.last_year + 1
        #                 target_semester['semester'] = subjectGroup.semester
        #             else:
        #                 l.error("Impossible event: The failed subject must be not in unstudied semester")
        #                 return -4
        #         else:
        #             l.error("The '"+grade_subject.subject.short_name+"' subject is pass, Do not allow to re-enroll")
        #             return -5
        #     else:
        #         # consider subject not study yet
        #         l.warn("Missing condition")
        #         l.info("previous_grade_subject " + extract_grade_subject(previous_grade_subject))
        #         l.info("grade_subject " + extract_grade_subject(grade_subject))
        #         return -6


    # def get_target_semester(self, previous_grade_subject, subject, prerequisite_name):
    #
    #     target_semester = dict()
    #     subjectGroup = models.SubjectGroup.objects(subject_id = subject.id,
    #                                                name = self.solution.member.subject_group).first()
    #     if subjectGroup is None:
    #         return -1
    #     original_semester_id = self.si.get(subjectGroup.year,
    #                                        subjectGroup.semester)
    #     # Consider the studied subject in the studied semester_id
    #
    #     if original_semester_id < self.solution.member.num_studied_semester_id:
    #         # This condition for fail subject only
    #         # Remark!!!!!!!
    #         # move to next year and same semester
    #         target_semester['year'] = self.solution.member.last_year + 1
    #         target_semester['semester'] = subjectGroup.semester
    #
    #     elif previous_grade_subject is None:
    #         l.error("Hereeeeeeeeeeee")
    #         target_semester['year'] = self.solution.member.last_year + 1
    #         target_semester['semester'] = subjectGroup.semester
    #     else:
    #         # move to next year and same semester from previous subject
    #         l.info(extract_grade_subject(previous_grade_subject))
    #
    #         if prerequisite_name is None:
    #             l.error('Must have prerequisite_name')
    #             return -2
    #         # initial target_semester
    #         target_semester['year'] = previous_grade_subject.year # + 1
    #         target_semester['semester'] = subjectGroup.semester
    #         check = True
    #         while check:
    #             target_grade_subject = models.GradeSubject(subject = subject,
    #                                                        year = target_semester['year'],
    #                                                        semester = target_semester['semester'])
    #             l.info(extract_grade_subject(target_grade_subject))
    #             l.info(target_semester['year'])
    #             p = prerequisites.selector(prerequisite_name, previous_grade_subject, target_grade_subject, self.solution.member)
    #             if p.canEnrolled() is True:
    #                 check = False
    #             else:
    #                 target_semester['year'] += 1
    #             if target_semester['year'] > self.solution.member.curriculum.required_num_year + 1:
    #                 # check = False
    #                 l.error('Can\'t find suitable semester id for %s', subject.name)
    #                 return -3
    #
    #     return self.si.get(target_semester['year'], target_semester['semester'])

    def find_fail_subjects(self):
        # interest only studied semester
        result_list = []
        # last_semester_id = self.si.get(self.solution.member.last_year, self.solution.member.last_semester) + 1
        for i in range(self.solution.member.num_studied_semester_id):
            for grade_subject in self.solution.semesters[i].subjects:
                if grade_subject.grade.mustReEnroll:
                    reenroll_subject = self.find_subject_in_not_studied_semester(grade_subject.subject)
                    result_list.append(models.GradeSubject(subject = grade_subject.subject,
                                                            year = reenroll_subject['year'],
                                                            semester = reenroll_subject['semester']))
                    # result_list.append(models.GradeSubject(subject = grade_subject.subject,
                    #                                         year = self.si.toYear(i),
                    #                                         semester = self.si.toSemester(i),
                    #                                         grade = grade_subject.grade))
        return result_list

    def find_subject_in_not_studied_semester(self, failSubject):
        # last_semester_id = self.si.get(self.solution.member.last_year, self.solution.member.last_semester) + 1
        for i in range(self.solution.member.num_studied_semester_id, len(self.solution.semesters)):
            # l.info('processing %s',i)
            for subject_order, subject_obj in enumerate(self.solution.semesters[i].subjects):
                if failSubject == subject_obj.subject:
                    return {
                        'semester_id': i,
                        'subject_order': subject_order,
                        'year': self.solution.semesters[i].year,
                        'semester': self.solution.semesters[i].semester
                    }
        return None

