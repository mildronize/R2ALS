from r2als import config
from r2als import models

class Prerequisite:
    # subject 1 ,subject 2 must be models.Subject
    def __init__(self,subject_1, subject_2):
        self.subject_1 = subject_1
        self.subject_2 = subject_2

class StudiedPrerequisite(Prerequisite):


class PassedPrerequisite(Prerequisite):


class Corequisite(Prerequisite):


class Cocurrent(Prerequisite):
