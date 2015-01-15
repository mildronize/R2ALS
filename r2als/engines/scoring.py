# return a score of the curriculum
# Zero score is best
# Much score is worst

# parameter

from r2als.libs.functions import SemesterIndex
from r2als.libs.logs import Log

l = Log('scoring').getLogger()

class Scoring:
    def __init__(self, semesterList):
        print("runnig scoring")
        self.mSemesters = semesterList.semesters
        self.member = semesterList.member
        # end before year 4 semester 3
        si = SemesterIndex(self.member.curriculum.num_semester)
        self.expectedSemesterToEnd = si.get(self.member.expected_year,self.member.expected_semester)
        # score will be increased if the user study more than over
        self.scorePerSemester = 100

    def count_semester(self):
        count = len(self.mSemesters)
        for i in range(len(self.mSemesters)-1,-1,-1):
            count -= 1
            if self.mSemesters[i].subjects != []:
                return count
        return count

    def scoring_semester(self):
        diff_semester = self.count_semester() - self.expectedSemesterToEnd
        #todo: missing conidition
        # if diff_semester < 0:
        l.info(self.count_semester())
        l.info(self.expectedSemesterToEnd)
        if diff_semester >= 0:
            return diff_semester * self.scorePerSemester
        else:
            return -1

    def process(self):
        totalScore = 0
        totalScore += self.scoring_semester()
        return totalScore

# def scoring(data):
#     totalScore = 0
#     # for i in reversed(range(1,len(data))):
#     i = len(data) - 1
#     while i > 0 :
#         if data[i-1] < data[i]:
#             totalScore += 1
#         i -= 1
#     return totalScore
