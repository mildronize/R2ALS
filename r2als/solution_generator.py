import copy

from r2als import config
from r2als import models
from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex

l = Log('solution_generator').getLogger()

class SolutionGeneratorMethod:

    def swap_gradeSubject(self, gs1, gs2):
        l.info('Swap sth')

    def moveGradeSubject(self, source_semester, source_subject_order, target_semester):
        l.info('Moving "%s"(%d/%d) to (%d/%d)', self.mSemesters[source_semester].subjects[source_subject_order].subject.name,
                                                self.si.toYear(source_semester),
                                                self.si.toSemester(source_semester),
                                                self.si.toYear(target_semester),
                                                self.si.toSemester(target_semester))
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
                    semester_id = models.SemesterId(year = self.si.toYear(i),
                                                    semester = self.si.toSemester(i))
                    lists.append(models.GradeSubject(subject = gradeSubject.subject, semester_id = semester_id))
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

    def getTargetSemester(self, subject ,last_year, last_semester, source_iden):
        last_semester_id = self.si.get(last_year, last_semester) + 1
        # subject_info = models.StubjectGroup.objects().first()
        subjectGroup = models.SubjectGroup.objects(subject_id = subject.id,
                                                   name = self.member.subject_group).first()
        if subjectGroup is None:
            return -2
        semester_id = self.si.get(subjectGroup.semester_id.year,
                                  subjectGroup.semester_id.semester)
        # l.info("%d [ ] %d", semester_id, last_semester_id)
        source_year = self.si.toYear(source_iden['semester_id'])
        source_semester = self.si.toSemester(source_iden['semester_id'])
        if semester_id < last_semester_id:
            # move to next year and same semester
            return self.si.get(last_year + 1, subjectGroup.semester_id.semester)
        else :
            # remark!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            return semester_id

    def prepareToMove(self, previous_subject, subject):
        l.info(">> %s", subject.short_name)
        source_iden = self.findSubject(subject)
        if source_iden is not None:
            target_semester = self.getTargetSemester(subject, self.member.last_year, self.member.last_semester, source_iden)
            if target_semester < 0:
                l.error('Impossible enroll of %s', subject.name)
            else :
                self.moveGradeSubject(source_iden['semester_id'],
                                      source_iden['subject_order'],
                                      target_semester)
        else:
            l.error('Not found subject %s', subject.name)

    def runSameChain(self, previous_subject, subject):
        # l.info("Create new runSameChain : %s", subject.short_name)
        if subject.reverse_prerequisites is []:
            return 0
        else:
            for reverse_prerequisite in subject.reverse_prerequisites:
                l.info(subject.short_name)
                self.prepareToMove(previous_subject, reverse_prerequisite.subject)
                self.runSameChain(subject, reverse_prerequisite.subject)

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
            self.prepareToMove(None, failGradeSubject.subject)
            self.runSameChain(None, failGradeSubject.subject)

        # find fail_subject
        #   In each loop: swap the fail subject to nearest semester
        #

        return self.mSemesters

class SolutionGenerator:

    def __ini__(self):
        l.info('Creating new Solution')
        self.start()

    def start(self):
        l.info('processing....')
        # self.a/lgorithm_likes_human()
        # return
