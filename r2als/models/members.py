
import mongoengine as me
import datetime


class Member(me.Document):
    meta = {'collection': 'members'}

    member_id = me.StringField(required=True)
    name = me.StringField(required=True)
    curriculum = me.ReferenceField('Curriculum')
    studied_group = me.StringField()
    registered_year = me.IntField(required=True)
    last_year = me.IntField(required=True)
    last_semester = me.IntField(required=True)
