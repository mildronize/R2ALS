__author__ = 'mildronize'

from r2als.libs.functions import SemesterIndex
import hashlib
from r2als.libs.logs import Log

l = Log('TabuHandler').getLogger()

class TabuHandler:

    def __init__(self, tabu_size):

        self.tabu_list = []
        self.tabu_size = tabu_size

        l.info("TabuHandler")

    def add_next_solution(self, solution):
        if self.is_existed(solution):
            return False
        self.store_solution(solution)
        return True

    def find_solution(self, str):
        if any(str in s for s in self.tabu_list):
            return True
        return False

    def is_exited(self, solution):
        if self.find_solution(self.generate_solution_id(solution)):
            return True
        return False

    def generate_solution_id(self, solution):
        return hashlib.sha1(self.convertSolution2String(solution)).hexdigest()

    def convertSolution2String(self, solution):
        result = ""
        for iter_semester in solution.semesters:
            result += ">%s/%s: " % (str(iter_semester.year), str(iter_semester.semester))
            for iter_gradeSubject in iter_semester.subjects:
                result += "(%s,%s) " % (iter_gradeSubject.subject.code, iter_gradeSubject.subject.name)
        # strLists =   ",".join(str(x) for x in soloution)
        # strLists_bytes = strLists.encode('utf-8')
        return result

    def store_solution(self, solution):
        if len(self.tabu_list) < self.tabu_size:
            self.tabu_list.append(self.generate_solution_id(solution))
        else:
            self.tabu_list.pop(0)
