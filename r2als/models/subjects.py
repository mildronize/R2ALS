
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

class StudiedGroup(me.Document):
    meta = {'collection': 'studied_groups'}

    name = me.StringField(required=True)
    year = me.IntField()
    semester = me.IntField()
    subject = me.ReferenceField('Subject')
    curriculum = me.ReferenceField('Curriculum')
    # subject temp info
    code = me.StringField()


    def clean(self):
        """Ensures that the StudiedGroup name found in the curriculum"""
        available_names = self.curriculum.studied_groups
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
    studied_groups = me.ListField(me.StringField(required=True, primary_key=True))
    categories = me.ListField(me.StringField(required=True, primary_key=True))

class Subject(me.Document):
    meta = {'collection': 'subjects'}

    code = me.StringField()
    name = me.StringField(required=True)
    credit = me.IntField(required=True)
    categories = me.ListField(me.StringField(required=True))
    curriculum = me.ReferenceField('Curriculum')
    # studied_prerequisite = me.ListField(me.ReferenceField('Subject'))
    # passed_prerequisite = me.ListField(me.ReferenceField('Subject'))
    # corequisite = me.ListField(me.ReferenceField('Subject'))
    # cocurrent = me.ListField(me.ReferenceField('Subject'))
    # prerequisites = me.ListField(me.ReferenceField('Prerequisite'))
    prerequisites = me.ListField(me.EmbeddedDocumentField(Prerequisite))
    reverse_prerequisites = me.ListField(me.EmbeddedDocumentField(Prerequisite))
    studied_groups = me.ListField(me.ReferenceField('StudiedGroup'))
    # studied_groups = me.SortedListField(me.EmbeddedDocumentField(StudiedGroup), ordering="name")
    # studied_groups = me.DictField()

    # studied_group = me.StringField()
    # year = me.IntField()
    # semester = me.IntField()
    isSpecific = me.BooleanField(required=True)
    # registration_date = me.DateTimeField(
    #     required=True, default=datetime.datetime.now)
    # updated_date = me.DateTimeField(
    #     required=True, default=datetime.datetime.now)
    # def add_studied_groups(self, studied_group_name, year, semester):
    #     # import pprint
    #     # pp = pprint.PrettyPrinter(indent=4)
    #     # pp.pprint(self.__dict__)
    #     available_names = self.curriculum.studied_groups
    #     if studied_group_name not in available_names:
    #         raise me.ValidationError('['+self.name+'] The name "'+self.name+'"'+ ' must in '+str(available_names))
    #     if studied_group_name in self.studied_groups.keys():
    #         raise me.ValidationError('['+self.name+'] The name "'+studied_group_name+'"'+ ' is exist')
    #     self.studied_groups[studied_group_name] = {
    #         'year' : year,
    #         'semester' : semester
    #     }

    def clean(self):
        """Ensures that the StudiedGroup name found in the curriculum"""
        available_categories = self.curriculum.categories
        # print(available_names)
        for category in self.categories:
            if category not in available_categories:
                raise me.ValidationError('The name "'+category+'"'+ ' must in '+str(available_categories))
    # def get_studied_group(self, studied_group_name):
    #     for studied_group in self.studied_groups:
    #         if studied_group_name == studied_group.name:
    #             return studied_group
    #     return None
    # def get_studied_group_order(self, studied_group_name):
    #     for i in range(len(self.studied_groups)):
    #         if studied_group_name == self.studied_groups[i].name:
    #             return i


# class Category(me.Document):
#     meta = {'collection': 'categories'}
#
#     name = me.StringField(required=True)
