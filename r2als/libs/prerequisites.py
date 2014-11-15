from r2als import config
from r2als import models
from r2als.libs.logs import Log

class Prerequisite:
    # subject 1 ,subject 2 must be models.gradeSubject
    def __init__(self,gradeSubjectt_1, gradeSubject_2):
        self.gradeSubjectt_1 = gradeSubjectt_1
        self.gradeSubject_2 = gradeSubject_2

class StudiedPrerequisite(Prerequisite):


class PassedPrerequisite(Prerequisite):


class Corequisite(Prerequisite):


class Cocurrent(Prerequisite):
