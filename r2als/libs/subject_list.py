__author__ = 'mildronize'

from r2als import models
from random import randint
from r2als.libs.logs import Log

l = Log('SubjectList').getLogger()


class SubjectList:

    def __init__(self):
        print("Running SelectingSubjects...")
        self.subject_list = []

    def add(self, subject):
        self.subject_list.append(subject)

    def get_subject(self, index):
        return self.subject_list[index]

    def get_subject_randomly(self):
        index = randint(0,len(self.subject_list))
        return self.subject_list[index]

