from r2als.libs.logs import Log
from r2als.libs.functions import SemesterIndex

l = Log('prerequisites').getLogger()

# gradeSubject = gs
def selector(prerequisite_name, gradeSubject_1, gradeSubject_2, member):
    if prerequisite_name == "studied_prerequisite":
        return StudiedPrerequisite(gradeSubject_1, gradeSubject_2, member)
    elif prerequisite_name == "passed_prerequisite":
        return PassedPrerequisite(gradeSubject_1, gradeSubject_2, member)
    elif prerequisite_name == "corequisite":
        return Corequisite(gradeSubject_1, gradeSubject_2, member)
    elif prerequisite_name == "cocurrent":
        return Cocurrent(gradeSubject_1, gradeSubject_2, member)

class Prerequisite:
    # subject 1 ,subject 2 must be models.gradeSubject
    # subject 1 ,subject 2 must be models.gs

    def __init__(self, grade_subject_before, grade_subject_after, member):
        self.gs_1 = grade_subject_before
        self.gs_2 = grade_subject_after
        self.member = member

        self.si = SemesterIndex()

    def canEnrolled(self):
        return False

    def _has_grade(self):
        if 'grade' in self.gs_1:
            if self.gs_1.grade is None:
                return False
            return True
        else:
            return False


    def _check_semester(self, less, equal):
        cmp_semester = self.si.compare_semester(self.gs_1.year,
                                                self.gs_1.semester,
                                                self.gs_2.year,
                                                self.gs_2.semester)
        if cmp_semester > 0:
            return False
        elif cmp_semester < 0:
            return less
        else:
            return equal


class StudiedPrerequisite(Prerequisite):

    def canEnrolled(self):
        # all grade without 'W'
        # StudiedPrerequisite
        if self._check_semester(less = True, equal = False) == False:
            return False

        if self._has_grade():
            if self.gs_1.grade.name == 'W':
                return False
            else:
                return True
        return True

class PassedPrerequisite(Prerequisite):

    def canEnrolled(self):
        #The prerequisite subject with at least grade D or S.
        if self._check_semester(less = True, equal = False) == False:
            return False
        # PassedPrerequisite
        if self._has_grade():
            if 'score' in self.gs_1.grade:
                if self.gs_1.grade.score >= 1.00 :
                    return True
                else:
                    return False
            elif self.gs_1.grade.name == 'S':
                return True
            else: return False
        return True

class Corequisite(Prerequisite):

    def canEnrolled(self):
        # The prerequisite subject is enrolled with the subject
        # simultaneously, or studied prerequisite subject
        if self._check_semester(less = True, equal = True) == False:
            return False

        if self._has_grade():
            if self.gs_1.grade.name == 'W':
                return False
            else:
                return True
        return True

# remark!!!!!!!!!!!!!
class Cocurrent(Prerequisite):

    # def isEnrolledSubject(self, gs):
    #     for enrolled_semester in self.member.enrolled_semesters:
    #         for gradeSubject in enrolled_semester.subjects:
    #             if gs.subject == gradeSubject.subject:
    #                 return gradeSubject.grade
    #     return None

    def canEnrolled(self):
        # Both 2 subjects must be enrolled simultaneously in first time

        if self._check_semester(less = False, equal = True) == False:
            return False
        return True
