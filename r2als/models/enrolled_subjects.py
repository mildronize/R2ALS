
import mongoengine as me
import datetime


class EnrolledSubject(me.Document):
    meta = {'collection': 'enrolled_subjects'}

    faculty = me.StringField(required=True)
    department = me.StringField(required=True)
    year = me.IntField(required=True)
