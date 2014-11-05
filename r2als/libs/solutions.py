
from r2als import models
import pprint

from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex
pp = pprint.PrettyPrinter(indent=4)
l = Log('libs/solutions').getLogger()

class InitialSolution:

    member = None
    semesterItems = []
    validSemesterList = []
    curriculum = None
    semesterIndex = None
    def __init__(self, curriculum, member):
        self.member = member
        self.curriculum = curriculum
        # === Todo ===: Remove all his subject!
        self.semesterIndex = SemesterIndex(curriculum.num_semester)
        self.initialEmptySemester()

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
            l.error("This semester is added")
            exit()
        self.semesterItems[self.semesterIndex.get(year,semester)]["subjects"] = subjects

    def addSemesterModel(self, semesterItem):
        mSemester = models.Semester()
        mSemester.member = self.member
        mSemester.year = semesterItem['year']
        mSemester.semester = semesterItem['semester']

        # Read all subject from same curriculum
        subjects = models.Subject.objects(curriculum = self.curriculum, year = semesterItem['year'], semester = semesterItem['semester'])
        for subject in subjects:
            if subject.studied_group == self.member.studied_group or subject.studied_group == "":
                # print(subject.name + " "+ subject.studied_group+ " ==> "+ str(subject.year)+"/"+str(subject.semester))
                gradeSubject = models.GradeSubject()
                gradeSubject.subject = subject
                if 'subjects' in semesterItem:
                    # l.debug("This semester(",semesterItem['year'],"/"+str(semesterItem['semester'])+") is studied")
                    # If the subject is enrolled, loading it into GradeSubject object
                    for subjectSemester in semesterItem['subjects']:
                        if subject.code == subjectSemester['code']:
                            gradeSubject.grade = subjectSemester['grade']
                            break
                # else: l.debug("This semester("+str(semesterItem['year'])+"/"+str(semesterItem['semester'])+") is not studied")
                gradeSubject.save()
                mSemester.subjects.append(gradeSubject)
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
                l.info("year("+str(self.semesterItems[i]['year'])+") & semester("+str(self.semesterItems[i]['semester'])+") are processing...")
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
