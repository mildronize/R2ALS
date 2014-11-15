
import mongoengine as me
import datetime

prerequisite_names = ['studied_prerequisite',
                      'passed_prerequisite',
                      'corequisite',
                      'cocurrent']

class Prerequisite(me.EmbeddedDocument):
    name = me.StringField(required=True,
                          choices= prerequisite_names,
                          primary_key=True)
    subject = me.ReferenceField('Subject')

class SubjectGroup(me.Document):
    meta = {'collection': 'subject_groups'}

    name = me.StringField(required=True)
    year = me.IntField()
    semester = me.IntField()
    subject = me.ReferenceField('Subject')
    curriculum = me.ReferenceField('Curriculum')
    # subject temp info
    code = me.StringField()


    def clean(self):
        """Ensures that the SubjectGroup name found in the curriculum"""
        available_names = self.curriculum.subject_groups
        # print(available_names)
        if self.name not in available_names:
            raise me.ValidationError('The name "'+self.name+'"'+ ' must in '+str(available_names))
        if self.subject is not None: self.code = self.subject.code

class Curriculum(me.Document):
    meta = {'collection': 'curriculums'}

    faculty = me.StringField(required=True)
    department = me.StringField(required=True)
    year = me.IntField(required=True)
    required_num_year = me.IntField(required=True) # A number of year must be studied
    num_semester = me.IntField(required=True)
    subject_groups = me.ListField(me.StringField(required=True, primary_key=True))
    categories = me.ListField(me.StringField(required=True, primary_key=True))

class Subject(me.Document):
    meta = {'collection': 'subjects'}

    code = me.StringField()
    name = me.StringField(required=True)
    credit = me.IntField(required=True)
    categories = me.ListField(me.StringField(required=True))
    curriculum = me.ReferenceField('Curriculum')
    prerequisites = me.ListField(me.EmbeddedDocumentField(Prerequisite))
    reverse_prerequisites = me.ListField(me.EmbeddedDocumentField(Prerequisite))
    subject_groups = me.ListField(me.ReferenceField('SubjectGroup'))

    isSpecific = me.BooleanField(required=True)
    # registration_date = me.DateTimeField(
    #     required=True, default=datetime.datetime.now)
    # updated_date = me.DateTimeField(
    #     required=True, default=datetime.datetime.now)

    def clean(self):
        """Ensures that the SubjectGroup name found in the curriculum"""
        available_categories = self.curriculum.categories
        # print(available_names)
        for category in self.categories:
            if category not in available_categories:
                raise me.ValidationError('The name "'+category+'"'+ ' must in '+str(available_categories))
