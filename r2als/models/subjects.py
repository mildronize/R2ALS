
import mongoengine as me
import datetime
from . import GradeSubject
# from .members import SemesterId

# prerequisite_names = ['studied_prerequisite',
#                       'passed_prerequisite',
#                       'corequisite',
#                       'cocurrent']

class Prerequisite(me.EmbeddedDocument):
    name = me.StringField(required=True,
                          # choices= prerequisite_names,
                          primary_key=True)
    # old version will be removed in the future
    subject = me.ReferenceField('Subject')

    grade_subject = me.EmbeddedDocumentField(GradeSubject)

    def clean(self):
        if self.name not in self.subject.curriculum.prerequisite_names:
            raise me.ValidationError('prerequisite_names(%s) not allow in this curriculum' % self.name)

class SubjectGroup(me.Document):
    meta = {'collection': 'subject_groups'}

    name = me.StringField(required=True)
    year = me.IntField()
    semester = me.IntField()
    # semester_id = me.EmbeddedDocumentField(SemesterId)
    subject = me.ReferenceField('Subject')
    curriculum = me.ReferenceField('Curriculum')
    # subject temp info
    code = me.StringField()
    subject_id = me.ObjectIdField('Subject')

    def clean(self):
        """Ensures that the SubjectGroup name found in the curriculum"""
        available_names = self.curriculum.subject_groups
        # print(available_names)
        if self.name not in available_names:
            raise me.ValidationError('The name "'+self.name+'"'+ ' must in '+str(available_names))
        if self.subject is not None:
            self.code = self.subject.code
            self.subject_id = self.subject.id

    def get_grade_subject(self):
        return GradeSubject(
            subject=self.subject,
            year=self.year,
            semester=self.semester
        )

class Curriculum(me.Document):
    meta = {'collection': 'curriculums'}

    faculty = me.StringField(required=True)
    department = me.StringField(required=True)
    year = me.IntField(required=True)

    required_num_year = me.IntField(required=True) # A number of year must be studied
    num_semester = me.IntField(required=True)
    max_year = me.IntField(required=True)
    num_required_semester_id = me.IntField()
    not_force_enrolled_semesters = me.ListField(me.IntField(min_value=1))
    min_credit_each_type = me.DictField()

    subject_groups = me.ListField(me.StringField(required=True, primary_key=True))
    categories = me.ListField(me.StringField(required=True, primary_key=True))

    prerequisite_names = me.ListField(me.StringField(required=True))
    branches = me.ListField(me.StringField(required=True))

    def clean(self):
        from r2als.libs.functions import SemesterIndex
        si = SemesterIndex(self.num_semester)
        self.num_required_semester_id = si.get(self.required_num_year, self.num_semester) + 1

class Subject(me.Document):
    meta = {'collection': 'subjects'}

    code = me.StringField()
    name = me.StringField(required=True)
    short_name = me.StringField()
    credit = me.IntField(required=True)
    categories = me.ListField(me.StringField(required=True))
    # If curriculum field is None, it means the subject not in any curriculum
    curriculum = me.ReferenceField('Curriculum')
    prerequisites = me.ListField(me.EmbeddedDocumentField(Prerequisite))
    reverse_prerequisites = me.ListField(me.EmbeddedDocumentField(Prerequisite))
    subject_groups = me.ListField(me.ReferenceField('SubjectGroup'))
    tags = me.ListField(me.StringField(required=True))
    not_fix_semester = me.BooleanField(required=True)
    isSpecific = me.BooleanField(required=True)
    is_approved = me.BooleanField(required=True, default=True)
    # is slot of subject , non-slot subject is extra subject not fix in study plan
    is_slot = me.BooleanField(required=True, default=True)
    not_fix_type = me.StringField()
    # If branch is none, it means no branch subject
    branch = me.StringField(default=None)

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
