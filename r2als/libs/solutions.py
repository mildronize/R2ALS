
import copy
import pprint
from mongoengine import Q

from r2als import models


from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex
from r2als.libs import next_solution_methods
pp = pprint.PrettyPrinter(indent=4)
l = Log('libs/solutions').getLogger()

class InitialSolution(next_solution_methods.MoveWholeChain):


    def __init__(self, member):
        self.solution = PreInitialSolution(member).start()
        # self.mSemesters = solution.semesters
        # self.member = member
        self.si = SemesterIndex(member.curriculum.num_semester)

    def start(self):
        # step 1 : find fail subject
        # step 2 : store it in list
        fail_subjects = self.find_fail_subjects()
        # for gradeSubject in fail_subject:
        #     l.info(gradeSubject.subject.short_name)
        # step 3 : move back each semester
        # Loop in remaining semester

        for failGradeSubject in fail_subjects:
            self.move_subject_whole_chain(None, failGradeSubject)

        self.move_non_related_subject_out()

        # solution = dict()
        # solution['member'] = self.member
        # solution['semesters'] = self.mSemesters

        # solution = models.Solution()
        # solution.member = self.member
        # solution.semesters = self.mSemesters
        self.solution.get_ready()
        self.solution.update_all_prerequisite()
        return self.solution


class PreInitialSolution:

    def __init__(self, member):
        # self.semesterItems = []
        self.member = member
        self.curriculum = member.curriculum
        self.importedSubject = []
        # === Todo ===: Remove all his subject!
        self.si = SemesterIndex(self.curriculum.num_semester)
        # self.maxStudiedSemesterIndex = self.si.get(self.member.last_year, self.member.last_semester)
        self.numStudiedSemesterIndex = self.member.num_studied_semester_id
        # self.maxSemesterIndex = self.si.get(self.curriculum.required_num_year, self.curriculum.num_semester)
        self.numSemesterIndex = self.curriculum.num_required_semester_id
        self.remainSubjects = []
        self.initialRemainSubjects()

        # self.initialEmptySemester()

    def initialRemainSubjects(self):
        for i in range(self.member.curriculum.num_semester):
            self.remainSubjects.append([])

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

    def addRemainSubjects(self, semester, gradeSubject):
        self.remainSubjects[semester-1].append(gradeSubject)

    def countRemainSubjects(self):
        tmp = 0
        for remainSubject in self.remainSubjects:
            tmp += len(remainSubject)
        return tmp

    def addSemesterModel(self, index, isRemaining = False):
        mSemester = models.Semester()
        mSemester.member = self.member
        mSemester.year = self.si.toYear(index)
        mSemester.semester = self.si.toSemester(index)

        if not isRemaining:
            # Read all subject from same curriculum
            # for studied semester index
            if index < self.numStudiedSemesterIndex:

                for enrolled_semester in self.member.enrolled_semesters:
                    if enrolled_semester.year == mSemester.year and \
                    enrolled_semester.semester == mSemester.semester:
                        mSemester.subjects = copy.copy(enrolled_semester.subjects)
                        break
            # for not studied semester index
            else:
                mSubjectGroups = models.SubjectGroup.objects(curriculum = self.curriculum,
                                                             name = self.member.subject_group,
                                                             year = mSemester.year,
                                                             semester = mSemester.semester)
                for mSubjectGroup in mSubjectGroups:
                    if not self.hasImportedSubject(str(mSubjectGroup.subject['id'])):
                        gradeSubject = models.GradeSubject()
                        gradeSubject.subject = mSubjectGroup.subject
                        mSemester.subjects.append(gradeSubject)
                        self.addImportedSubject(str(mSubjectGroup.subject['id']))
        else:
            for gradeSubject in self.remainSubjects[index-self.numSemesterIndex]:
                mSemester.subjects.append(models.GradeSubject(subject = gradeSubject.subject))

        return mSemester

    def start(self):
        # mSemesters = []
        solution = models.Solution()
        mSemesters = solution.semesters
        for i in range(self.numSemesterIndex):
            y = self.si.toYear(i)
            s = self.si.toSemester(i)
            numSubjects = models.SubjectGroup.objects(curriculum = self.curriculum,
                                                      name = self.member.subject_group ,
                                                      year = y,
                                                      semester = s).count()
            mSemesters.append(self.addSemesterModel(i, False))
            if i < self.numStudiedSemesterIndex:
                # ==========  This section for year & semester which are studied ========
                l.info("semster (%d/%d) which are stuided, are processing[%d]",y,s,numSubjects)
            else:
                # ==========  This section for year & semester remaining ========
                l.info("semster (%d/%d) are processing[%d]",y,s,numSubjects)
        for gradeSubject in solution.findNotEnrolledSubjects():
            print(gradeSubject.subject.short_name)
            self.addRemainSubjects(gradeSubject.semester, gradeSubject)
        print(self.countRemainSubjects())
        # add extra semester
        # if len(self.remainSubjects[]) > 0:
        if self.countRemainSubjects() > 0:

            for i in range(self.numSemesterIndex,
                           self.numSemesterIndex + self.curriculum.num_semester):
                y = self.si.toYear(i)
                s = self.si.toSemester(i)
                mSemesters.append(self.addSemesterModel(i, True))

        solution.member = self.member
        return solution

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
