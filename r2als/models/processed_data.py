
import mongoengine as me
import datetime


class Semester(me.Document):
    meta = {'collection': 'semesters'}

    subjects = me.ListField(me.ReferenceField('GradeSubject'))
    member = me.ReferenceField('Member')
    year = me.IntField(required=True)
    semester = me.IntField(required=True)

class GradeSubject(me.Document):
    meta = {'collection': 'grade_subjects'}

    subject = me.ReferenceField('Subject')
    grade = me.StringField()
