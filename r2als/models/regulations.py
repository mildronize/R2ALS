
import mongoengine as me
import datetime


class Grade(me.Document):
    meta = {'collection': 'grades'}

    name = me.StringField(required=True, primary_key=True)
    score = me.FloatField()
    isCredit = me.BooleanField(required=True, default = True)
    canReEnroll = me.BooleanField(required=True, default = True)
    mustReEnroll = me.BooleanField(required=True)
    isEnrolled = me.BooleanField(required=True, default = True)
    curriculum = me.ReferenceField('Curriculum')
