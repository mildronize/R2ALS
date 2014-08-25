from .subjects import Subject, Category, Curriculum
from .members import Member
from .enrolled_subjects import EnrolledSubject

from mongoengine import connect


def initial(setting):
    connect(setting.get('mongodb.db_name'), host=setting.get('mongodb.host'))
