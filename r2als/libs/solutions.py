
from r2als import models
from mongoengine import Q
import pprint

from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex
pp = pprint.PrettyPrinter(indent=4)
l = Log('libs/solutions').getLogger()


class InitialSolution:

    def __init__(self, member):
        self.semesterItems = []
        self.member = member
        self.curriculum = member.curriculum
        self.importedSubject = []
        # === Todo ===: Remove all his subject!
        self.si = SemesterIndex(self.curriculum.num_semester)
        self.maxStudiedSemesterIndex = self.si.get(self.member.last_year, self.member.last_semester)
        self.numStudiedSemesterIndex = self.maxStudiedSemesterIndex + 1
        self.maxSemesterIndex = self.si.get(self.curriculum.required_num_year, self.curriculum.num_semester)
        self.numSemesterIndex = self.maxSemesterIndex + 1
        self.initialEmptySemester()

    # def convertGradeSubjectsModelToDict(self, gradeSubjects=[]):
    #     result = []
    #     for gradeSubject in gradeSubjects:
    #         result.append({
    #             'code': gradeSubject.subject.code,
    #             # 'id': gradeSubject.subject.id,
    #             'grade': gradeSubject.grade,
    #         })
    #     return result

    def isCorrectInitialSolution(self):
        for y in range(1,self.curriculum.required_num_year+1):
            for s in range(1,self.curriculum.num_semester+1):
                index = self.si.get(y,s)

                mSemester = models.Semester.objects(year = y, semester = s, member = self.member).first()
                # numSubjects = models.Subject.objects(Q(year = y, semester = s, curriculum = self.curriculum)  & ( Q(studied_group=self.member.studied_group) | Q(studied_group='') )).count()
                numSubjects = models.StudiedGroup.objects(curriculum = self.curriculum, year = y, semester = s,name='first-group').count()
                # studied semester
                if index < self.numStudiedSemesterIndex:
                    l.debug('checking Semester '+str(y)+'/'+str(s)+': Studied Semester')
                    if len(self.semesterItems[index]['subjects']) != len(mSemester.subjects):
                        l.error('Semester '+str(y)+'/'+str(s)+': Number of subject is not match')
                    else:
                        l.info('Number of subject is match')
                        if 'subjects' in mSemester:
                            raw_subjects = sorted(self.semesterItems[index]['subjects'], key=lambda k: k['code'])
                            gradeSubjects = sorted(mSemester.subjects, key=lambda gradeSubject: gradeSubject.subject.code)
                            # gradeSubjects = self.convertGradeSubjectsModelToDict(mSemester.subjects)
                            # gradeSubjects = sorted(gradeSubjects, key=lambda k: k['code'])
                            for i in range(len(mSemester.subjects)):
                                if raw_subjects[i]['code'] != gradeSubjects[i].subject.code:
                                    l.error('Raw: '+raw_subjects[i]['code']+' not equal '+gradeSubjects[i].subject.code)
                        else:
                            l.info('Not have subjects in the Semester')
                else:
                    # Future semester

                    l.debug('checking Semester '+str(y)+'/'+str(s))
                    # return True
                l.info ('numSubject: '+str(len(mSemester.subjects))+ '/' +str(numSubjects))
        return True


    def countAllSubject(self):
        # subjects = models.Subject.objects( Q(curriculum = self.curriculum) & ( Q(studied_group=self.member.studied_group) | Q(studied_group='')) )
        return models.StudiedGroup.objects(curriculum = self.curriculum, name='first-group').count()

    def countOnlyMemberSubject(self):
        semesters = models.Semester.objects(member = self.member)
        total = 0
        for semester in semesters:
            total += len(semester.subjects)
            # l.info(self.member.name +" has "+ str(total)+" subjects")
        return total

    def initialEmptySemester(self):
        for y in range(1,self.member.last_year+1):
            for s in range(1,self.member.last_semester+1):
                # print(str(y)+" " +str(s))
                semesterItem = {}
                semesterItem['year'] = y
                semesterItem['semester'] = s
                self.semesterItems.append(semesterItem)
        return True

    def printSemester(self):
        pp.pprint(self.semesterItems)

    def addStudiedSubject(self, year, semester, subjects):
        # subjects example data:
        #   [ {'code' : '200-101','grade' : 'C'},
        #     {'code' : '242-101','grade' : 'C'} ]
        for subject in subjects:
            if 'code' not in subject or 'grade' not in subject:
                l.error("Subject list must have code & grade")
                exit()

        if 'subjects' in self.semesterItems[self.si.get(year,semester)]:
            l.error("This semester is added")
        else:
            self.semesterItems[self.si.get(year,semester)]["subjects"] = subjects

    def countImportedSubject(self):
        l.debug(len(self.importedSubject))
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


    def addSemesterModel(self, semesterItems, index):
        mSemester = models.Semester()
        mSemester.member = self.member
        mSemester.year = self.si.toYear(index)
        mSemester.semester = self.si.toSemester(index)

        # Read all subject from same curriculum
        # for studied semester index
        if index < self.numStudiedSemesterIndex:
            semesterItem = semesterItems[index]
            for raw_subject in semesterItem['subjects']:
                # subject = models.Subject.objects( Q(curriculum = self.curriculum, code = raw_subject['code']) & ( Q(studied_group=self.member.studied_group) | Q(studied_group='')) ).first()
                studiedGroup = models.StudiedGroup.objects(curriculum = self.curriculum,
                                                      name = 'first-group' ,
                                                      code = raw_subject['code']).first()
                # if raw_subject['code'] in subject_groups.subject.code
                if studiedGroup is None:
                    l.error('Unknown the subject ' + raw_subject['code'] + ' in subjects collection(db)')
                else:
                    gradeSubject = models.GradeSubject()
                    gradeSubject.subject = studiedGroup.subject
                    gradeSubject.grade = raw_subject['grade']
                    # gradeSubject.save()
                    mSemester.subjects.append(gradeSubject)
                    self.addImportedSubject(str(studiedGroup.subject['id']))
        # for not studied semester index
        else:
            # subjects = models.Subject.objects( Q(curriculum = self.curriculum, year = mSemester.year, semester = mSemester.semester) & ( Q(studied_group=self.member.studied_group) | Q(studied_group='')) )
            studiedGroups = models.StudiedGroup.objects(curriculum = self.curriculum,
                                                   name = self.member.studied_group,
                                                   year = mSemester.year,
                                                   semester = mSemester.semester)
            l.debug(len(studiedGroups))
            for studiedGroup in studiedGroups:
                if not self.hasImportedSubject(str(studiedGroup.subject['id'])):
                    gradeSubject = models.GradeSubject()
                    gradeSubject.subject = studiedGroup.subject
                    # gradeSubject.save()
                    mSemester.subjects.append(gradeSubject)
                    self.addImportedSubject(str(studiedGroup.subject['id']))

        mSemester.save()

    def start(self):
        # check data before start
        l.debug('count-start: %s',self.countOnlyMemberSubject())
        for i in range(self.numSemesterIndex):
            y = self.si.toYear(i)
            s = self.si.toSemester(i)
            # numSubjects = models.Subject.objects(Q(year = y, semester = s, curriculum = self.curriculum)  & ( Q(studied_group=self.member.studied_group) | Q(studied_group='') )).count()
            numSubjects = models.StudiedGroup.objects(curriculum = self.curriculum,
                                                      name = self.member.studied_group ,
                                                      year = y,
                                                      semester = s).count()
            if i < self.numStudiedSemesterIndex:
                # ==========  This section for year & semester which are studied ========
                l.info("year("+str(y)+") & semester("+str(s)+") ,which are stuided, are processing["+str(numSubjects)+"]")
                l.debug('count..: %s',self.countOnlyMemberSubject())
                self.addSemesterModel(self.semesterItems, i)
                l.debug('countXX: %s',self.countOnlyMemberSubject())
            else:
                # ==========  This section for year & semester remaining ========
                l.info("year("+str(y)+") & semester("+str(s)+") are processing["+str(numSubjects)+"]")
                l.debug('count..: %s',self.countOnlyMemberSubject())
                self.addSemesterModel(self.semesterItems, i)
                l.debug('countXX: %s',self.countOnlyMemberSubject())
        l.debug('count-end: %s',self.countOnlyMemberSubject())
