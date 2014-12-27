import copy

from r2als import config
from r2als import models
from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex
from r2als.libs import prerequisites

l = Log('solution_generator').getLogger()

class SolutionGeneratorMethod:

    def swap_gradeSubject(self, gs1, gs2):
        l.info('Swap sth')

    def moveGradeSubject(self, source_semester, source_subject_order, target_semester):
        msg = 'Moving "%s"\t\t(%d/%d) to (%d/%d)' % ( self.mSemesters[source_semester].subjects[source_subject_order].subject.short_name,
                                                self.si.toYear(source_semester),
                                                self.si.toSemester(source_semester),
                                                self.si.toYear(target_semester),
                                                self.si.toSemester(target_semester))
        if source_semester ==  target_semester:
            l.error(msg)
        else:
            l.info(msg)

        tmp_gradeSubject = copy.copy(self.mSemesters[source_semester].subjects[source_subject_order])
        # move
        self.mSemesters[target_semester].subjects.append(tmp_gradeSubject)
        # remove
        self.mSemesters[source_semester].subjects.pop(source_subject_order)

class MoveSameChainBackwardOnly(SolutionGeneratorMethod):

    def __init__(self, semesterList):
        l.info('Runing MoveSameChainBackwardOnly ...')
        self.mSemesters = semesterList.semesters
        self.member = semesterList.member
        print(self.member)
        self.si = SemesterIndex(self.member.curriculum.num_semester)

    def findFailSubjects(self):
        # interest only studied semester
        lists = list()
        last_semester_id = self.si.get(self.member.last_year, self.member.last_semester) + 1
        for i in range(last_semester_id):
            for gradeSubject in self.mSemesters[i].subjects:
                if gradeSubject.grade.mustReEnroll:
                    lists.append(models.GradeSubject(subject = gradeSubject.subject,
                                                    year = self.si.toYear(i),
                                                    semester = self.si.toSemester(i),
                                                    grade = gradeSubject.grade))
        return lists

    def findSubject(self, failSubject):
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

    def getTargetSemester(self, previous_gradeSubject, subject ,last_year, last_semester, source_iden, prerequisite_name):
        target_semester = dict()
        last_semester_id = self.si.get(last_year, last_semester) + 1
        subjectGroup = models.SubjectGroup.objects(subject_id = subject.id,
                                                   name=self.member.subject_group).first()
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
        else :
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

    def prepareToMove(self, previous_gradeSubject, gradeSubject, prerequisite_name):
        if previous_gradeSubject is None:
            l.debug("START >> %s" , gradeSubject.subject.short_name)
        else:
            l.debug("%s (%s/%s) >> %s", previous_gradeSubject.subject.short_name,
                                        previous_gradeSubject.year,
                                        previous_gradeSubject.semester,
                                        gradeSubject.subject.short_name)
        source_iden = self.findSubject(gradeSubject.subject)
        if source_iden is not None:
            target_semester = self.getTargetSemester(previous_gradeSubject,
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

    def runSameChain(self, previous_gradeSubject, gradeSubject):
        # l.info("Create new runSameChain : %s", subject.short_name)
        subject = gradeSubject.subject
        if previous_gradeSubject is None:
            self.prepareToMove(None, gradeSubject, None)
        if subject.reverse_prerequisites is []:
            return 0
        else:
            for reverse_prerequisite in subject.reverse_prerequisites:
                semester_id = self.findSubject(subject)['semester_id']
                tmp_gradeSubject = models.GradeSubject(subject = subject,
                                                       year = self.si.toYear(semester_id),
                                                       semester = self.si.toSemester(semester_id),
                                                       )
                prerequisite_gradeSubject = models.GradeSubject(subject = reverse_prerequisite.subject)
                self.prepareToMove(tmp_gradeSubject, prerequisite_gradeSubject, reverse_prerequisite.name)
                self.runSameChain(tmp_gradeSubject, prerequisite_gradeSubject)

    def start(self):
        # step 1 : find fail subject
        # step 2 : store it in list
        fail_subject = self.findFailSubjects()
        # for gradeSubject in fail_subject:
        #     l.info(gradeSubject.subject.short_name)
        # step 3 : move back each semester
        # Loop in remaining semester
        last_semester_id = self.si.get(self.member.last_year, self.member.last_semester) + 1
        for failGradeSubject in fail_subject:
            self.runSameChain(None, failGradeSubject)

        # find fail_subject
        #   In each loop: swap the fail subject to nearest semester
        #


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

class SolutionGenerator:

    def __ini__(self):
        l.info('Creating new Solution')
        self.start()

    def start(self):
        l.info('processing....')
        # self.a/lgorithm_likes_human()
        # return

