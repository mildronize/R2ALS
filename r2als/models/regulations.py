
import mongoengine as me
import datetime


class Grade(me.Document):
    meta = {'collection': 'grades'}

    name = me.StringField(required=True)
    score = me.FloatField()
    isCredit = me.BooleanField(required=True)
    canReEnroll = me.BooleanField(required=True)
    isEnrolled = me.BooleanField(required=True)
