
import mongoengine as me
import datetime


class Subject(me.Document):
    meta = {'collection': 'subjects'}

    code = me.StringField()
    name = me.StringField(required=True)
    credit = me.IntField(required=True)
    categories = me.ListField(me.ReferenceField('Category'))
    curriculum = me.ReferenceField('Curriculum')
    studied_prerequisite = me.ListField(me.ReferenceField('Subject'))
    passed_prerequisite = me.ListField(me.ReferenceField('Subject'))
    corequisite = me.ListField(me.ReferenceField('Subject'))
    cocurrent = me.ListField(me.ReferenceField('Subject'))
    studied_group = me.StringField()

    # registration_date = me.DateTimeField(
    #     required=True, default=datetime.datetime.now)
    # updated_date = me.DateTimeField(
    #     required=True, default=datetime.datetime.now)

class Category(me.Document):
    meta = {'collection': 'categories'}

    name = me.StringField(required=True)

class Curriculum(me.Document):
    meta = {'collection': 'curriculums'}

    faculty = me.StringField(required=True)
    department = me.StringField(required=True)
    year = me.IntField(required=True)
    studied_groups = me.ListField(me.StringField())


# class StudiedGroup(me.Document):
#     meta = {'collection': 'studied_groups'}
#
#     name = me.StringField(required=True)
