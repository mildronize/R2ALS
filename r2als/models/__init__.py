from .subjects import Subject, Category, Curriculum
from .members import Member
from .enrolled_subjects import EnrolledSubject

from mongoengine import connect

def initial(setting):
    db = connect(setting.get('mongodb.db_name'), host=setting.get('mongodb.host'))
    if setting.get('mongodb.is_reset') :
        db.drop_database(setting.get('mongodb.db_name'))
