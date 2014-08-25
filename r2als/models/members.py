
import mongoengine as me
import datetime


class Member(me.Document):
    meta = {'collection': 'members'}

    id = me.StringField(required=True)
    name = me.StringField(required=True)
