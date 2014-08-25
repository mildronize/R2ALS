
import mongoengine as me
import datetime


class EnrolledSubject(me.Document):
    meta = {'collection': 'enrolled_subjects'}

    subject = me.ReferenceField('Subject')
    member = me.ReferenceField('Member')
    grade = me.FloatField(required=True)
