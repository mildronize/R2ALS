
import mongoengine as me
import datetime

class GradeSubject(me.EmbeddedDocument):

    subject = me.ReferenceField('Subject')
    grade = me.ReferenceField('Grade')

    # def clean(self):
    #     if self.grade not in Grade.objects().only('name'):
    #         raise me.ValidationError('The name "'+self.grade+'"'+ ' not allow')

class Semester(me.Document):
    meta = {'collection': 'semesters'}

    subjects = me.ListField(me.EmbeddedDocumentField(GradeSubject))
    member = me.ReferenceField('Member')
    year = me.IntField(required=True)
    semester = me.IntField(required=True)

class EnrolledSemester(me.EmbeddedDocument):
    meta = {'collection': 'semesters'}

    subjects = me.ListField(me.EmbeddedDocumentField(GradeSubject))
    year = me.IntField(required=True)
    semester = me.IntField(required=True)

class Member(me.Document):
    meta = {'collection': 'members'}

    member_id = me.StringField(required=True,primary_key=True)
    name = me.StringField(required=True)
    curriculum = me.ReferenceField('Curriculum')
    studied_group = me.StringField()
    registered_year = me.IntField(required=True)
    last_year = me.IntField(required=True)
    last_semester = me.IntField(required=True)

    enrolled_semesters = me.ListField(me.EmbeddedDocumentField(EnrolledSemester))
