
import mongoengine as me
import datetime

prerequisite_names = ['studied_prerequisite','passed_prerequisite','corequisite','cocurrent']

class Prerequisite(me.EmbeddedDocument):
    name = me.StringField(required=True, choices= prerequisite_names)
    subject = me.ReferenceField('Subject')

class StudiedGroup(me.EmbeddedDocument):
    # change to Document
    name = me.StringField(required=True, default = 'all')
    year = me.IntField()
    semester = me.IntField()
    # add subject

class Subject(me.Document):
    meta = {'collection': 'subjects'}

    code = me.StringField()
    name = me.StringField(required=True)
    credit = me.IntField(required=True)
    categories = me.ListField(me.ReferenceField('Category'))
    curriculum = me.ReferenceField('Curriculum')
    # studied_prerequisite = me.ListField(me.ReferenceField('Subject'))
    # passed_prerequisite = me.ListField(me.ReferenceField('Subject'))
    # corequisite = me.ListField(me.ReferenceField('Subject'))
    # cocurrent = me.ListField(me.ReferenceField('Subject'))
    # prerequisites = me.ListField(me.ReferenceField('Prerequisite'))
    prerequisites = me.ListField(me.EmbeddedDocumentField(Prerequisite))
    reverse_prerequisites = me.ListField(me.EmbeddedDocumentField(Prerequisite))
    studied_groups = me.ListField(me.EmbeddedDocumentField(StudiedGroup))
    # studied_group = me.StringField()
    # year = me.IntField()
    # semester = me.IntField()
    isSpecific = me.BooleanField(required=True)
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
    required_num_year = me.IntField(required=True) # A number of year must be studied
    studied_groups = me.ListField(me.StringField())
    num_semester = me.IntField(required=True)
