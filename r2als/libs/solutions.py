
from r2als import models
from mongoengine import Q
import pprint

from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex
pp = pprint.PrettyPrinter(indent=4)
l = Log('libs/solutions').getLogger()

class InitialSolution:


    def __init__(self, curriculum, member):
        self.semesterItems = []
        self.validSemesterList = []
        self.semesterIndex = None
        self.member = member
        self.curriculum = curriculum
        self.importedSubject = []
        # === Todo ===: Remove all his subject!
        self.semesterIndex = SemesterIndex(curriculum.num_semester)
        self.initialEmptySemester()

    def isCorrectInitialSolution(self):
        for y in range(1,self.curriculum.required_num_year+1):
            for s in range(1,self.curriculum.num_semester+1):
                if self.validSemesterList[self.semesterIndex.get(y,s)] == False: return True
                mSemester = models.Semester.objects(year = y, semester = s, member = self.member).first()
                if len(self.semesterItems[self.semesterIndex.get(y,s)]['subjects']) != len(mSemester.subjects):
                    l.error('Semester '+str(y)+'/'+str(s)+': Number of subject is not match')
                    l.debug('raw subject: ')
                    tmp = ''
                    for subject in self.semesterItems[self.semesterIndex.get(y,s)]['subjects']:
                        tmp += subject['code'] + ' '
                    l.debug(tmp)
                    l.debug('subject in db: ')
                    tmp = ''
                    for mSubject in mSemester.subjects:
                        tmp += mSubject.subject.code + ' '
                    l.debug(tmp)
                    return False
                else:
                    targeting_match = len(mSemester.subjects)
                    counting_match = 0
                    for mSubject in mSemester.subjects:
                        for raw_subject in self.semesterItems[self.semesterIndex.get(y,s)]['subjects']:
                            if mSubject.code == raw_subject.code:
                                counting_match += 1
                                break
                    if counting_match == targeting_match:
                        return True
                    else:
                        l.error('Semester '+str(y)+'/'+str(s)+': Subject is not match')
                        return False

        return True

    def countAllSubject(self):
        subjects = models.Subject.objects( Q(curriculum = self.curriculum) & ( Q(studied_group=self.member.studied_group) | Q(studied_group='')) )
        # l.debug(len(subjects))
        # i = 1
        # for subject in subjects:
        #     l.debug(str(subject.year) + '/' + str(subject.semester) + ':(' + str(i) + ') ' + subject.name)
        #     i = i + 1
        # l.info("There are " + str(len(subjects))+" subjects")
        return len(subjects)

    def countOnlyMemberSubject(self):
        semesters = models.Semester.objects( member = self.member)
        total = 0
        for semester in semesters:
            total += len(semester.subjects)
        # l.info(self.member.name +" has "+ str(total)+" subjects")
        return total

    def initialEmptySemester(self):
        for y in range(1,self.curriculum.required_num_year+1):
            for s in range(1,self.curriculum.num_semester+1):
                # print(str(y)+" " +str(s))
                semesterItem = {}
                semesterItem['year'] = y
                semesterItem['semester'] = s
                self.semesterItems.append(semesterItem)
        # initial validSemesterList
        for i in range(self.curriculum.num_semester * self.curriculum.required_num_year):
            self.validSemesterList.append(False)
        return True

    def printSemester(self):
        pp.pprint(self.semesterItems)

    def addStudiedSubject(self, year=1, semester=1, subjects=[]):
        # subjects example data:
        #   [ {'code' : '200-101','grade' : 'C'},
        #     {'code' : '242-101','grade' : 'C'} ]
        for subject in subjects:
            if 'code' not in subject or 'grade' not in subject:
                l.error("Subject list must have code & grade")
                exit()

        if self.validSemesterList[self.semesterIndex.get(year,semester)] == False:
            self.validSemesterList[self.semesterIndex.get(year,semester)] = True
        else:
            l.debug(self.validSemesterList)
            l.error("This semester is added")
            exit()
        self.semesterItems[self.semesterIndex.get(year,semester)]["subjects"] = subjects

    def hasImportedSubject(self, subject_code):
        if subject_code in self.importedSubject: return True
        else: return False

    def addImportedSubject(self, subject_code):
        if self.hasImportedSubject(subject_code) :
            l.error('The subject '+subject_code+'is exist !')
            return False
        else:
            self.importedSubject.append(subject_code)
            return True

    def addSemesterModel(self, semesterItem):
        mSemester = models.Semester()
        mSemester.member = self.member
        mSemester.year = semesterItem['year']
        mSemester.semester = semesterItem['semester']

        # Read all subject from same curriculum

        # for studied semester index
        if 'subjects' in semesterItem:
            for raw_subject in semesterItem['subjects']:
                subject = models.Subject.objects( Q(curriculum = self.curriculum, code = raw_subject['code']) & ( Q(studied_group=self.member.studied_group) | Q(studied_group='')) ).first()
                if subject is None:
                    l.error('Not found the subject ' + raw_subject.code + 'in subjects collection(db)')
                else:
                    gradeSubject = models.GradeSubject()
                    gradeSubject.subject = subject
                    gradeSubject.grade = raw_subject['grade']
                    gradeSubject.save()
                    mSemester.subjects.append(gradeSubject)
                    self.addImportedSubject(raw_subject['code'])

        # for not studied semester index
        else:
            subjects = models.Subject.objects( Q(curriculum = self.curriculum, year = semesterItem['year'], semester = semesterItem['semester']) & ( Q(studied_group=self.member.studied_group) | Q(studied_group='')) )
            for subject in subjects:
                if not self.hasImportedSubject(subject.code):
                    gradeSubject = models.GradeSubject()
                    gradeSubject.subject = subject
                    gradeSubject.save()
                    mSemester.subjects.append(gradeSubject)
                    self.addImportedSubject(subject.code)
        mSemester.save()

    def start(self):

        # ==========  This section for year & semester which are studied ========
        # check data before start
        target_checking = self.semesterIndex.get(self.member.last_num_year, self.member.last_semester)

        for i in range(target_checking + 1):
            if self.validSemesterList[i] == False:
                l.error("Please add subject all semester which you passed")
                exit()
            else:
                l.info("year("+str(self.semesterItems[i]['year'])+") & semester("+str(self.semesterItems[i]['semester'])+") ,which are stuided, are processing...")
                self.addSemesterModel(self.semesterItems[i])

        # ==========  This section for year & semester remaining ========

        for i in range(target_checking + 1, self.semesterIndex.get(self.curriculum.required_num_year, self.curriculum.num_semester) + 1):
            # comparing SemesterIndex with year , semester
            if self.semesterIndex.get(self.semesterItems[i]['year'], self.semesterItems[i]['semester']) != i:
                l.error("Somthing wrong about SemesterIndex not match with year("+str(self.semesterItems[i]['year'])+") & semester("+str(self.semesterItems[i]['semester'])+") ")
                exit()
            else:
                # l.info("year("+str(self.semesterItems[i]['year'])+") & semester("+str(self.semesterItems[i]['semester'])+") are processing...")
                self.addSemesterModel(self.semesterItems[i])


    # def start(self):
    #
    #     # ==========  This section for year & semester which are studied ========
    #     # check data before start
    #     target_checking = self.semesterIndex.get(self.member.last_num_year, self.member.last_semester)
    #     for i in range(target_checking + 1):
    #         if self.validSemesterList[i] == False:
    #             l.error("Please add subject all semester which u passed")
    #             exit()
    #         else:
    #             l.info("year("+str(self.semesterItems[i]['year'])+") & semester("+str(self.semesterItems[i]['semester'])+") ,which are stuided, are processing...")
    #
    #     # ==========  This section for year & semester remaining ========
    #
    #     for i in range(target_checking, self.semesterIndex.get(self.curriculum.required_num_year, self.curriculum.num_semester)):
    #         # comparing SemesterIndex with year , semester
    #         if self.semesterIndex.get(self.semesterItems[i]['year'], self.semesterItems[i]['semester']) != i:
    #             l.error("Somthing wrong about SemesterIndex not match with year("+str(self.semesterItems[i]['year'])+") & semester("+str(self.semesterItems[i]['semester'])+") ")
    #             exit()
    #         else:
    #             l.info("year("+str(self.semesterItems[i]['year'])+") & semester("+str(self.semesterItems[i]['semester'])+") are processing...")
    #
    #         mSemester = models.Semester()
    #         mSemester.member = self.member
    #         mSemester.year = self.semesterItems[i]['year']
    #         mSemester.semester = self.semesterItems[i]['semester']
    #
    #         # Read all subject from same curriculum
    #         subjects = models.Subject.objects(curriculum = self.curriculum, year = self.semesterItems[i]['year'], semester =  self.semesterItems[i]['semester'])
    #         for subject in subjects:
    #             if subject.studied_group == self.member.studied_group or subject.studied_group == "":
    #                 # print(subject.name + " "+ subject.studied_group+ " ==> "+ str(subject.year)+"/"+str(subject.semester))
    #                 gradeSubject = models.GradeSubject()
    #                 # If the subject is enrolled, loading it into GradeSubject object
    #                 for subjectSemester in self.semesterItems[i]['subjects']:
    #                     if subject.code == subjectSemester['code']:
    #                         gradeSubject.grade = subjectSemester['grade']
    #                         break
    #                 gradeSubject.save()
    #                 mSemester.subjects.append(gradeSubject)
    #         mSemester.save()
