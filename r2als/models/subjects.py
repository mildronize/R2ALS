
import mongoengine as me
import datetime


class Subject(me.Document):
    meta = {'collection': 'subjects'}

    id = me.StringField(required=True)
    name = me.StringField(required=True)
    credit = me.IntField(required=True)
    category = me.ReferenceField('Category')
    curriculum = me.ReferenceField('Curriculum')
    studied_prerequisite = me.ListField(me.ReferenceField('Subject'))
    passed_prerequisit = me.ListField(me.ReferenceField('Subject'))
    corequisite = me.ListField(me.ReferenceField('Subject'))
    cocurrent = me.ListField(me.ReferenceField('Subject'))

    # registration_date = me.DateTimeField(
    #     required=True, default=datetime.datetime.now)
    # updated_date = me.DateTimeField(
    #     required=True, default=datetime.datetime.now)

class Category(me.Document):
    meta = {'collection': 'categories'}

    name = me.StringField(required=True)
