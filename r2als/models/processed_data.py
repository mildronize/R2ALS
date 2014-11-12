
import mongoengine as me
import datetime

class GradeSubject(me.EmbeddedDocument):
    # meta = {'collection': 'grade_subjects'}

    subject = me.ReferenceField('Subject')
    grade = me.StringField()


class Semester(me.Document):
    meta = {'collection': 'semesters'}

    subjects = me.ListField(me.EmbeddedDocumentField(GradeSubject))
    member = me.ReferenceField('Member')
    year = me.IntField(required=True)
    semester = me.IntField(required=True)
