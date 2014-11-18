from r2als import config
from r2als import models
from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex

l = Log('prerequisites').getLogger()

# gradeSubject = gs

class Prerequisite:
    # subject 1 ,subject 2 must be models.gradeSubject
    # subject 1 ,subject 2 must be models.gs

    def __init__(self, gradeSubject_1, gradeSubject_2, member):
        self.gs_1 = gradeSubject_1
        self.gs_2 = gradeSubject_2
        self.member = member

        self.si = SemesterIndex()

    def canEnrolled(self):
        return False

    def check_semester(self, less, equal):
        if self.si.compare_SemesterId(self.gs_1.semester_id,
                                      self.gs_2.semester_id) > 0:
            return False
        elif self.si.compare_SemesterId(self.gs_1.semester_id,
                                        self.gs_2.semester_id) < 0:
            return less
        else:
            return equal


class StudiedPrerequisite(Prerequisite):

    def canEnrolled(self):
        # all grade without 'W'
        # StudiedPrerequisite
        if self.check_semester(less = True, equal = False) == False:
            return False
        print(self.gs_1.__dict__)
        if self.gs_1.grade.name == 'W':
            return False
        else:
            return True

class PassedPrerequisite(Prerequisite):

    def canEnrolled(self):
        #The prerequisite subject with at least grade D or S.
        if self.check_semester(less = True, equal = False) == False:
            return False
        # PassedPrerequisite
        if 'score' in self.gs_1.grade:
            if self.gs_1.grade.score >= 1.00 :
                return True
            else:
                return False
        elif self.gs_1.grade.name == 'S':
            return True
        else: return False

class Corequisite(Prerequisite):

    def canEnrolled(self):
        # The prerequisite subject is enrolled with the subject
        # simultaneously, or studied prerequisite subject
        if self.check_semester(less = True, equal = True) == False:
            return False

        if self.gs_1.grade.name == 'W':
            return False
        else:
            return True

class Cocurrent(Prerequisite):

    def isEnrolledSubject(self, gs):
        for enrolled_semester in self.member.enrolled_semesters:
            for gradeSubject in enrolled_semester.subjects:
                if gs.subject == gradeSubject.subject:
                    return gradeSubject.grade
        return None

    def canEnrolled(self):
        # Both 2 subjects must be enrolled simultaneously in first time
        # case 3 : Both subject1 & subject 2 are not enrolled
        # if self.findEnrolledSubject(self.gs_1) is None and self.findEnrolledSubject(self.gs_2) is None:

        # case 1 : subject1 was enrolled & subject2 got 'W' must re-enroll
        # case 2 : subject1 got 'W' must re-enroll & subject2 was enrolled



        if self.check_semester(less = False, equal = True) == False:
            return False
