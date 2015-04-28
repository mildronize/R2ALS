
import copy
import pprint
from mongoengine import Q

from r2als import models

from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex, extract_grade_subject
from r2als.libs.next_solution_methods import MoveWholeChain, MoveSubjectOut
from r2als.engines.validator import validator

pp = pprint.PrettyPrinter(indent=4)
l = Log('libs/solutions').getLogger()

class InitialSolution:

    def __init__(self, member, random_operator):
        si = SemesterIndex(member.curriculum.num_semester)
        self.solution = PreInitialSolution(member).get_solution()
        # # l.info("Last semester %d/%d" % (si.toYear(len(self.solution.semesters)-1), si.toSemester(len(self.solution.semesters)-1) ) )
        self.solution = MoveWholeChain(self.solution).get_initial_solution()
        self.solution = MoveSubjectOut(self.solution).get_solution(random_operator)
        self.solution.get_ready()
        self.solution.min_semester_id = len(self.solution.semesters) - 1
        if validator(self.solution, ['*']) is False:
            self.solution = MoveWholeChain(self.solution).get_solution()
            self.solution.get_ready()

    def get_solution(self):
        return self.solution

class PreInitialSolution:

    def __init__(self, member):
        self.member = member
        self.curriculum = member.curriculum
        # initial all values
        self.imported_subject = []
        # === Todo ===: Remove all his subject!
        self.si = SemesterIndex(self.curriculum.num_semester)
        # self.maxStudiedSemesterIndex = self.si.get(self.member.last_year, self.member.last_semester)
        self.numStudiedSemesterIndex = self.member.num_studied_semester_id
        # self.maxSemesterIndex = self.si.get(self.curriculum.required_num_year, self.curriculum.num_semester)
        self.numSemesterIndex = self.curriculum.num_required_semester_id
        l.info("Last semester %d/%d" % (self.si.toYear(self.numSemesterIndex-1), self.si.toSemester(self.numSemesterIndex-1) ) )
        self.remain_subjects = self.initial_empty_year()

    def initial_empty_year(self):
        subjects = []
        for i in range(self.member.curriculum.num_semester):
            subjects.append([])
        return subjects

    def has_imported_subject(self, subject_id):
        if subject_id in self.imported_subject: return True
        else: return False

    def add_imported_subject(self, subject_id):
        if self.has_imported_subject(subject_id) :
            # mSubject = models.Subject.objects(id= subject_id).first()
            l.info('The subject '+subject_id+'is exist ! ')
            return False
        else:
            self.imported_subject.append(subject_id)
            return True

    def count_remain_subjects(self):
        tmp = 0
        for remain_subject in self.remain_subjects:
            tmp += len(remain_subject)
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

                        for grade_subject in enrolled_semester.subjects:
                            self.add_imported_subject(str(grade_subject.subject.id))
                        break
            # for not studied semester index
            else:
                mSubjectGroups = models.SubjectGroup.objects(curriculum = self.curriculum,
                                                             name = self.member.subject_group,
                                                             year = mSemester.year,
                                                             semester = mSemester.semester)
                for mSubjectGroup in mSubjectGroups:
                    if not self.has_imported_subject(str(mSubjectGroup.subject['id'])):
                        gradeSubject = models.GradeSubject()
                        gradeSubject.subject = mSubjectGroup.subject
                        mSemester.subjects.append(gradeSubject)
                        self.add_imported_subject(str(mSubjectGroup.subject['id']))
        else:
            for gradeSubject in self.remain_subjects[index-self.numSemesterIndex]:
                mSemester.subjects.append(models.GradeSubject(subject = gradeSubject.subject))

        return mSemester

    def get_solution(self):
        solution = models.Solution()
        mSemesters = solution.semesters
        # initail fail subject
        for i in range(self.numSemesterIndex):
            y = self.si.toYear(i)
            s = self.si.toSemester(i)
            numSubjects = models.SubjectGroup.objects(curriculum = self.curriculum,
                                                      name = self.member.subject_group,
                                                      year = y,
                                                      semester = s).count()
            mSemesters.append(self.addSemesterModel(i, False))
            if i < self.numStudiedSemesterIndex:
                # ==========  This section for year & semester which are studied ========
                l.info("semster (%d/%d) which are stuided, are processing[%d]",y,s,numSubjects)
            else:
                # ==========  This section for year & semester remaining ========
                l.info("semster (%d/%d) are processing[%d]",y,s,numSubjects)

        for gradeSubject in solution.findFailSubjects():
            self.remain_subjects[gradeSubject.semester-1].append(gradeSubject)

        grade_subjects = []
        for grade_subject in solution.get_grade_subjects():
            grade_subjects.append(str(grade_subject.subject.id))
        all_subjects = []
        for subject_group in models.SubjectGroup.objects(curriculum = self.member.curriculum,name = self.member.subject_group):
            all_subjects.append(str(subject_group.subject.id))

        # checking importing subject
        tmp_diff_lists = list(set(grade_subjects) - set(all_subjects))
        if len(tmp_diff_lists) > 0:
            for tmp_subject in tmp_diff_lists:
                l.info(models.Subject.objects(id=tmp_subject).first().short_name +
                       "\t\t is enrolled over than the curriculum")

        # checking missing subject
        missing_subjects = list(set(all_subjects) - set(grade_subjects))
        missing_grade_subjects = []

        l.info(len(missing_subjects))
        if len(missing_subjects) > 0:
            for missing_subject in missing_subjects:
                subject = models.Subject.objects(id=missing_subject).first()
                l.info(subject.short_name +"\t is missing")
                subject_group = models.SubjectGroup.objects(subject_id=subject.id,
                                                            curriculum= self.member.curriculum,
                                                            name = self.member.subject_group).first()
                if subject_group is not None:
                    tmp_grade_subject = models.GradeSubject(subject=subject_group.subject,
                                                            year=subject_group.year,
                                                            semester=subject_group.semester)
                    self.remain_subjects[tmp_grade_subject.semester-1].append(tmp_grade_subject)
                    missing_grade_subjects.append(models.GradeSubject(subject=subject_group.subject))
                else:
                    l.error("Can't find subject")

        # add extra semester
        # if len(self.remainSubjects[]) > 0:
        l.info("self.countRemainSubjects() " + str(self.count_remain_subjects()))
        if self.count_remain_subjects() > 0:

            for i in range(self.numSemesterIndex,
                           self.numSemesterIndex + self.curriculum.num_semester):
                mSemesters.append(self.addSemesterModel(i, True))

        solution.member = self.member
        solution.get_ready()
        solution.update_all_prerequisite()
        solution = MoveWholeChain(solution).get_initial_solution(missing_grade_subjects)
        # solution.update_all_prerequisite()
        return solution

    # def differenceTwoList(self, list1, list2):
    #     if(len(list1) > len(list2)):
    #         return list(set(list1) - set(list2))
    #     return list(set(list2) - set(list1))

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
