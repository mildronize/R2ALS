
import mongoengine as me
import datetime
from r2als.libs.functions import *
from r2als.libs.logs import Log
l = Log('models/members').getLogger()
# import math

# class SemesterId(me.EmbeddedDocument):
# #     semester_id = me.IntField()
#     year = me.IntField()
#     semester = me.IntField()
#     num_semester = me.IntField(required=True)
#
#     def clean(self):
#         from r2als.libs.functions import SemesterId
#         semester_id = SemesterId(self.num_semester)
#         if self.year is None and self.semester is None:
#             if self.semester_id is None:
#                 raise me.ValidationError('Please input "semester_id" or (year,semester)')
#                 # print('')
#             else:
#                 self.year = semester_id.toYear(self.semester_id)
#                 self.semester = semester_id.toSemester(self.semester_id)
#         elif self.year is not None and self.semester is not None:
#             self.semester_id = semester_id.get(self.year,self.semester)
#         else:
#             # print('')
#             raise me.ValidationError('Please input (year,semester)')
#         # raise me.ValidationError('test cleaning')

class GradeSubject(me.EmbeddedDocument):

    subject = me.ReferenceField('Subject')
    grade = me.ReferenceField('Grade')
    year = me.IntField()
    semester = me.IntField()
    # semester_id = me.EmbeddedDocumentField(SemesterId)

class Solution(me.Document):

    # todo: Making dynamic number of semesters list

    meta = {'collection': 'solutions'}
    member = me.ReferenceField('Member', primary_key= True)
    semesters = me.ListField(me.ReferenceField('Semester'))

    def get_ready(self):
        self.update_all_grade_subject()
        self.remove_empty_semester()

    def remove_empty_semester(self):
        for i in reversed(range(len(self.semesters))):
            if len(self.semesters[i].subjects) is 0:
                self.semesters.pop(i)
            else:
                break
    def extend_semester_size(self, target_semester_id):
        si = SemesterIndex(self.member.curriculum.num_semester)
        if target_semester_id > len(self.semesters)-1:
            l.error("Extending semester size")
            for i in range(len(self.semesters)-1, target_semester_id):
                tmp = Semester(subjects=[],
                               member=self.member,
                               year=si.toYear(i),
                               semester=si.toSemester(i))
                self.semesters.append(tmp)

    def update_all_grade_subject(self):
        for semester in self.semesters:
            for grade_subject in semester.subjects:
                grade_subject.year = semester.year
                grade_subject.semester = semester.semester

    def update_all_prerequisite(self):
        from r2als.libs.logs import Log
        l = Log('members/Solution').getLogger()
        for semester in self.semesters:
            for grade_subject in semester.subjects:
                for prerequisite in grade_subject.subject.prerequisites:
                    found_grade_subject = self.__find_grade_subject(prerequisite.subject)
                    if found_grade_subject is not None:
                        prerequisite.grade_subject = found_grade_subject
                    else:
                        l.error("Not found subject")
                for reverse_prerequisite in grade_subject.subject.reverse_prerequisites:
                    found_grade_subject = self.__find_grade_subject(reverse_prerequisite.subject)
                    if found_grade_subject is not None:
                        reverse_prerequisite.grade_subject = found_grade_subject
                    else:
                        l.error("Not found subject")



    # def move_grade_subject(self, grade_subject, target_semester_id):
    #     # Prepare var
    #     si = SemesterIndex(self.member.curriculum.num_semester)
    #     semester_id = si.get(grade_subject.year, grade_subject.semester)
    #     target_subject_position = self.__find_grade_subject_id(semester_id,
    #                                                            grade_subject.subject)
    #     # Moving
    #     self.semesters[target_semester_id].subjects.append(
    #         self.semesters[semester_id].subjects.pop(target_subject_position)
    #     )
    def get_enrolled_grade_subjects(self):
        # count all subject without grade 'W'
        # num_subject = 0
        tmp = list()
        for semester in self.semesters:
            for gradeSubject in semester.subjects:
                if 'grade' in gradeSubject:
                    if gradeSubject.grade.isEnrolled:
                        tmp.append(gradeSubject)
                else:
                    tmp.append(gradeSubject)
        return tmp

    def get_grade_subjects(self):
        tmp = list()
        for semester in self.semesters:
            for gradeSubject in semester.subjects:
                tmp.append(gradeSubject)
        return tmp

    def countNumEnrolledSubject(self):
        return len(self.get_enrolled_grade_subjects())

    def findFailSubjects(self):
        # return a list of subject with grade 'W'
        lists = list()
        for semester in self.semesters:
            for gradeSubject in semester.subjects:
                if 'grade' in gradeSubject:
                    if gradeSubject.grade.mustReEnroll:
                        gradeSubject.year = semester.year
                        gradeSubject.semester = semester.semester
                        lists.append(gradeSubject)
        return lists

    def __find_grade_subject(self, subject):
        for semester in self.semesters:
            for grade_subject in semester.subjects:
                if subject == grade_subject.subject:
                    return grade_subject
        return None


class Semester(me.Document):
    meta = {'collection': 'semesters'}

    subjects = me.ListField(me.EmbeddedDocumentField(GradeSubject))
    member = me.ReferenceField('Member')
    year = me.IntField(required=True)
    semester = me.IntField(required=True)

    def find_non_related_subjects(self):
        non_related_grade_subjects = []
        for gradeSubject in self.subjects:
            if gradeSubject.subject.prerequisites == [] and \
            gradeSubject.subject.reverse_prerequisites == []:
                # add subject into subject_list
                non_related_grade_subjects.append(gradeSubject)
        return non_related_grade_subjects

    def calculate_total_credit(self):
        total = 0
        for gradeSubject in self.subjects:
            total += gradeSubject.subject.credit
        return total


    # semester_id = me.EmbeddedDocumentField(SemesterId)

class EnrolledSemester(me.EmbeddedDocument):

    subjects = me.ListField(me.EmbeddedDocumentField(GradeSubject))
    year = me.IntField(required=True)
    semester = me.IntField(required=True)
    # semester_id = me.EmbeddedDocumentField(SemesterId)

class Member(me.Document):
    meta = {'collection': 'members'}

    member_id = me.StringField(required=True,primary_key=True)
    name = me.StringField(required=True)
    curriculum = me.ReferenceField('Curriculum')
    subject_group = me.StringField()
    registered_year = me.IntField(required=True)

    # Last studied semester id
    last_year = me.IntField(required=True)
    last_semester = me.IntField(required=True)
    num_studied_semester_id = me.IntField()

    # Expected semester id
    # expected_year = me.IntField(required=True)
    # expected_semester = me.IntField(required=True)
    # num_expected_semester_id = me.IntField()

    # margin credit that user allow extra total credit
    # margin_credit = me.IntField(required=True)

    enrolled_semesters = me.ListField(me.EmbeddedDocumentField(EnrolledSemester))

    def clean(self):
        from r2als.libs.functions import SemesterIndex
        si = SemesterIndex(self.curriculum.num_semester)
        self.num_studied_semester_id = si.get(self.last_year, self.last_semester) + 1
        # self.num_expected_semester_id = si.get(self.expected_year, self.expected_semester) + 1