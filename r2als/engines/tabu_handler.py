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
        if self.__is_existed(solution):
            return False
        self.__store_solution(solution)
        return True

    def __find_solution(self, str):
        if any(str in s for s in self.tabu_list):
            return True
        return False

    def __is_existed(self, solution):
        l.info(self.__generate_solution_id(solution))
        if self.__find_solution(self.__generate_solution_id(solution)):
            return True
        return False

    def __generate_solution_id(self, solution):
        return hashlib.sha1(self.__convert_solution_to_string(solution)).hexdigest()

    def __convert_solution_to_string(self, solution):
        result = ""
        for iter_semester in solution['semesters']:
            result += ">%s/%s: " % (str(iter_semester.year), str(iter_semester.semester))
            for iter_gradeSubject in iter_semester.subjects:
                result += "(%s,%s) " % (iter_gradeSubject.subject.code, iter_gradeSubject.subject.name)
        return result.encode('utf-8')

    def __store_solution(self, solution):
        if len(self.tabu_list) == self.tabu_size:
            self.tabu_list.pop(0)
            l.info("Tabu is full. Removing oldest solution from Tabu List (size %d)" % (self.tabu_size))
        self.tabu_list.append(self.__generate_solution_id(solution))
        return True
