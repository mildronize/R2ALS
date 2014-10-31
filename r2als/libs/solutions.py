from r2als import models
import pprint
pp = pprint.PrettyPrinter(indent=4)
num_semester = 3

def toSemesterIndex(year, semester):
    return ((year-1) * num_semester + semester) - 1

class InitialSolution:

    member = None
    semesterItems = []
    validSemesterList = []
    curriculum = None
    def __init__(self, curriculum, member):
        self.member = member
        self.curriculum = curriculum
        # === Todo ===: Remove all his subject!

        self.initialEmptySemester()
        # initial validSemesterList
        for i in range(num_semester * self.curriculum.required_num_year):
            self.validSemesterList.append(False)

    def initialEmptySemester(self):
        for y in range(1,self.curriculum.required_num_year+1):
            for s in range(1,num_semester+1):
                # print(str(y)+" " +str(s))
                semesterItem = {}
                semesterItem['year'] = y
                semesterItem['semester'] = s
                self.semesterItems.append(semesterItem)

    def printSemester(self):
        pp.pprint(self.semesterItems)

    def addStudiedSubject(self, year=1, semester=1, subjects=[]):
        # subjects example data:
        #   [ {'code' : '200-101','grade' : 'C'},
        #     {'code' : '242-101','grade' : 'C'} ]
        for subject in subjects:
            if 'code' not in subject or 'grade' not in subject:
                print("Error: subject list must have code & grade")
                exit()

        if self.validSemesterList[toSemesterIndex(year,semester)] == False:
            self.validSemesterList[toSemesterIndex(year,semester)] = True
        else:
            print("Error! This semester is added")
            exit()
        self.semesterItems[toSemesterIndex(year,semester)]["subjects"] = subjects

    def start(self):

        # check data before start
        target_checking = toSemesterIndex(self.member.last_num_year, self.member.last_semester)
        for i in range(target_checking + 1):
            if self.validSemesterList[i] == False:
                print("Error! please add subject all semester which u passed")
                exit()

        for semesterItem in self.semesterItems:

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
                    # If the subject is enrolled, loading it into GradeSubject object
                    for subjectSemester in semesterItem['subjects']:
                        if subject.code == subjectSemester['code']:
                            gradeSubject.grade = subjectSemester['grade']
                            break
                    gradeSubject.save()
                    mSemester.subjects.append(gradeSubject)
            mSemester.save()
