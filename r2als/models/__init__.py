from .subjects import Subject, Curriculum, Prerequisite, StudiedGroup
from .members import Member, Semester, GradeSubject, EnrolledSemester
from .regulations import Grade

from mongoengine import connect

def initial(setting):
    db = connect(setting.get('mongodb.db_name'), host=setting.get('mongodb.host'))
    # print(setting.get('mongodb.remove_collections'))
    if setting.get('mongodb.is_drop_database') is not None:
        if setting.get('mongodb.is_drop_database') is True:
            db.drop_database(setting.get('mongodb.db_name'))
    elif setting.get('mongodb.is_reset') :
        db.drop_database(setting.get('mongodb.db_name'))
