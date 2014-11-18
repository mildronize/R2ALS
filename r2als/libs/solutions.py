
import copy
import pprint
from mongoengine import Q

from r2als import models


from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex
pp = pprint.PrettyPrinter(indent=4)
l = Log('libs/solutions').getLogger()

class InitialSolution:

    def __init__(self, member):
        # self.semesterItems = []
        self.member = member
        self.curriculum = member.curriculum
        self.importedSubject = []
        # === Todo ===: Remove all his subject!
        self.si = SemesterIndex(self.curriculum.num_semester)
        self.maxStudiedSemesterIndex = self.si.get(self.member.last_year, self.member.last_semester)
        self.numStudiedSemesterIndex = self.maxStudiedSemesterIndex + 1
        self.maxSemesterIndex = self.si.get(self.curriculum.required_num_year, self.curriculum.num_semester)
        self.numSemesterIndex = self.maxSemesterIndex + 1
        # self.initialEmptySemester()

    def countImportedSubject(self):
        # l.debug(len(self.importedSubject))
        return len(self.importedSubject)

    def hasImportedSubject(self, subject_id):
        if subject_id in self.importedSubject: return True
        else: return False

    def addImportedSubject(self, subject_id):
        if self.hasImportedSubject(subject_id) :
            mSubject = models.Subject.objects(id= subject_id).first()
            l.error('The subject '+subject_id+'is exist !: '+mSubject.name)
            return False
        else:
            self.importedSubject.append(subject_id)
            return True

    def addSemesterModel(self, index):
        mSemester = models.Semester()
        mSemester.member = self.member
        mSemester.semester_id = models.SemesterId(year = self.si.toYear(index),
                                                  semester = self.si.toSemester(index))

        # Read all subject from same curriculum
        # for studied semester index
        if index < self.numStudiedSemesterIndex:

            for enrolled_semester in self.member.enrolled_semesters:
                if enrolled_semester.semester_id.year == mSemester.semester_id.year and \
                enrolled_semester.semester_id.semester == mSemester.semester_id.semester:
                    mSemester.subjects = copy.copy(enrolled_semester.subjects)
                    break
        # for not studied semester index
        else:
            mSubjectGroups = models.SubjectGroup.objects(curriculum = self.curriculum,
                                                         name = self.member.subject_group,
                                                         semester_id__year = mSemester.semester_id.year,
                                                         semester_id__semester = mSemester.semester_id.semester)
            for mSubjectGroup in mSubjectGroups:
                if not self.hasImportedSubject(str(mSubjectGroup.subject['id'])):
                    gradeSubject = models.GradeSubject()
                    gradeSubject.subject = mSubjectGroup.subject
                    mSemester.subjects.append(gradeSubject)
                    self.addImportedSubject(str(mSubjectGroup.subject['id']))

        return mSemester

    def start(self):
        mSemesters = []
        for i in range(self.numSemesterIndex):
            y = self.si.toYear(i)
            s = self.si.toSemester(i)
            numSubjects = models.SubjectGroup.objects(curriculum = self.curriculum,
                                                      name = self.member.subject_group ,
                                                      semester_id__year = y,
                                                      semester_id__semester = s).count()
            mSemesters.append(self.addSemesterModel(i))
            if i < self.numStudiedSemesterIndex:
                # ==========  This section for year & semester which are studied ========
                l.info("semster (%d/%d) which are stuided, are processing[%d]",y,s,numSubjects)
            else:
                # ==========  This section for year & semester remaining ========
                l.info("semster (%d/%d) are processing[%d]",y,s,numSubjects)
        return mSemesters

# def isCorrectInitialSolution(self):
#     for y in range(1,self.curriculum.required_num_year+1):
#         for s in range(1,self.curriculum.num_semester+1):
#             index = self.si.get(y,s)
#             l.info('semester (%d/%d) ....',y,s)
#             mSemester = models.Semester.objects(year = y,
#                                                 semester = s,
#                                                 member = self.member).first()
#             if mSemester is None:
#                 semester = models.Semester.objects(year = y,
#                                         semester = s)
#                 if semester is not None: pp.pprint(semester)
#                 l.error('semester (%d/%d) not found',y,s)
#                 pp.pprint(self.member.__dict__)
#                 exit()
#
#             numSubjects = models.SubjectGroup.objects(curriculum = self.curriculum, year = y, semester = s,name='first-group').count()
#             # studied semester
#             if index < self.numStudiedSemesterIndex:
#                 l.debug('checking Semester '+str(y)+'/'+str(s)+': Studied Semester')
#                 if len(self.semesterItems[index]['subjects']) != len(mSemester.subjects):
#                     l.error('Semester '+str(y)+'/'+str(s)+': Number of subject is not match')
#                 else:
#                     l.info('Number of subject is match')
#                     if 'subjects' in mSemester:
#                         raw_subjects = sorted(self.semesterItems[index]['subjects'], key=lambda k: k['code'])
#                         gradeSubjects = sorted(mSemester.subjects, key=lambda gradeSubject: gradeSubject.subject.code)
#                         # gradeSubjects = self.convertGradeSubjectsModelToDict(mSemester.subjects)
#                         # gradeSubjects = sorted(gradeSubjects, key=lambda k: k['code'])
#                         for i in range(len(mSemester.subjects)):
#                             if raw_subjects[i]['code'] != gradeSubjects[i].subject.code:
#                                 l.error('Raw: '+raw_subjects[i]['code']+' not equal '+gradeSubjects[i].subject.code)
#                     else:
#                         l.info('Not have subjects in the Semester')
#             else:
#                 # Future semester
#
#                 l.debug('checking Semester '+str(y)+'/'+str(s))
#                 # return True
#             if 'subjects' in mSemester:
#                 num_subject_mSemester = len(mSemester.subjects)
#             else: num_subject_mSemester = 0
#             l.info ('numSubject: '+str(num_subject_mSemester)+ '/' +str(numSubjects))
#     return True

# def countAllSubject(self):
#     # subjects = models.Subject.objects( Q(curriculum = self.curriculum) & ( Q(subject_group=self.member.subject_group) | Q(subject_group='')) )
#     return models.SubjectGroup.objects(curriculum = self.curriculum, name='first-group').count()
#
# def countOnlyMemberSubject(self):
#     semesters = models.Semester.objects(member = self.member)
#     total = 0
#     # l.debug('start 0')
#     for semester in semesters:
#         total += len(semester.subjects)
#         # l.debug('counting (%d/%d) = %d',semester.year, semester.semester, len(semester.subjects))
#     # l.debug('end %d',total)
#     return total

# def initialEmptySemester(self):
#     for y in range(1,self.member.last_year+1):
#         for s in range(1,self.member.last_semester+1):
#             # print(str(y)+" " +str(s))
#             semesterItem = {}
#             semesterItem['year'] = y
#             semesterItem['semester'] = s
#             self.semesterItems.append(semesterItem)
#     return True

# def printSemester(self):
#     pp.pprint(self.semesterItems)

# def addStudiedSubject(self, year, semester, subjects):
#     # subjects example data:
#     #   [ {'code' : '200-101','grade' : 'C'},
#     #     {'code' : '242-101','grade' : 'C'} ]
#     for subject in subjects:
#         if 'code' not in subject or 'grade' not in subject:
#             l.error("Subject list must have code & grade")
#             exit()
#
#     if 'subjects' in self.semesterItems[self.si.get(year,semester)]:
#         l.error("This semester is added")
#     else:
#         self.semesterItems[self.si.get(year,semester)]["subjects"] = subjects
