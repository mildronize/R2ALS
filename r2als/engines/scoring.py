# return a score of the curriculum
# Zero score is best
# Much score is worst

# parameter

from r2als.libs.functions import SemesterIndex
from r2als.libs.logs import Log

l = Log('scoring').getLogger()

class Scoring:
    def __init__(self, solution):
        print("runnig scoring")
        self.mSemesters = solution.semesters
        self.member = solution.member
        # end before year 4 semester 3
        self.si = SemesterIndex(self.member.curriculum.num_semester)

        # self.scorePerSemester = 100

    def __count_semester(self):
        count = len(self.mSemesters)
        for i in range(len(self.mSemesters)-1,-1,-1):
            count -= 1
            if self.mSemesters[i].subjects != []:
                return count
        return count

    def _scoring_semester(self, expected_semester_to_end, score_per_semester):
        diff_semester = self.__count_semester() - expected_semester_to_end
        #todo: missing conidition
        # if diff_semester < 0:
        # l.info(self.__count_semester())
        # l.info(expected_semester_to_end)
        if diff_semester >= 0:
            return diff_semester * score_per_semester
        else:
            return 0

    def get_score(self):
        totalScore = 10
        # parameter
        score_per_semester = 100
        expected_semester_to_end = self.si.get(self.member.curriculum.required_num_year , self.member.curriculum.num_semester)
        # expected_semester_to_end = self.si.get(5,1)

        # score will be increased if the user study more than over
        # static scoring
        totalScore += self._scoring_semester(expected_semester_to_end, score_per_semester)
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
