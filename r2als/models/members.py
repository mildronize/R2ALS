
import mongoengine as me
import datetime
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

class SemestersList(me.Document):
    meta = {'collection': 'semesters_lists'}
    member = me.ReferenceField('Member', primary_key= True)
    semesters = me.ListField(me.ReferenceField('Semester'))

    def countNumEnrolledSubject(self):
        # count all subject without grade 'W'
        num_subject = 0
        for semester in self.semesters:
            for gradeSubject in semester.subjects:
                # print(semester.semester_id.year, semester.semester_id.semester,gradeSubject.subject.short_name)
                if 'grade' in gradeSubject:
                    if gradeSubject.grade.isEnrolled:
                        num_subject += 1
                        # print(num_subject,': ',gradeSubject.subject.short_name)
                else:
                    num_subject += 1
                    # print(num_subject,': ',gradeSubject.subject.short_name)
        return num_subject

    def findNotEnrolledSubjects(self):
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


class Semester(me.Document):
    meta = {'collection': 'semesters'}

    subjects = me.ListField(me.EmbeddedDocumentField(GradeSubject))
    member = me.ReferenceField('Member')
    year = me.IntField(required=True)
    semester = me.IntField(required=True)
    # semester_id = me.EmbeddedDocumentField(SemesterId)

class EnrolledSemester(me.EmbeddedDocument):
    meta = {'collection': 'semesters'}

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
    last_year = me.IntField(required=True)
    last_semester = me.IntField(required=True)

    enrolled_semesters = me.ListField(me.EmbeddedDocumentField(EnrolledSemester))
