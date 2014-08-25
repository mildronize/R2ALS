from .subjects import Subject, Category
from .curriculums import Curriculum

from mongoengine import connect


def initial(setting):
    connect(setting.get('mongodb.db_name'), host=setting.get('mongodb.host'))
    
