__author__ = 'mildronize'

from r2als.libs.functions import SemesterIndex
import hashlib
from r2als.libs.logs import Log

l = Log('TabuManager').getLogger()

class TabuManager:

    def __init__(self, tabu_size):
        self.tabu_list = []
        self.tabu_size = tabu_size
        l.info("TabuManager")

    def add_next_solution(self, solution):
        if self.__is_existed(solution):
            l.info("Exist solution is found")
            return False
        self.__store_solution(solution)
        return True

    def __find_solution(self, str):
        if any(str in s for s in self.tabu_list):
            return True
        return False

    def __is_existed(self, solution):
        # l.info(self.__generate_solution_id(solution))
        if self.__find_solution(self.__generate_solution_id(solution)):
            return True
        return False

    def __generate_solution_id(self, solution):
        return hashlib.sha1(self.__convert_solution_to_string(solution)).hexdigest()

    # def __convert_solution_to_string(self, solution):
    #     result = ""
    #     for i in range( solution.member.num_studied_semester_id , len(solution.semesters)):
    #         iter_semester = solution.semesters[i]
    #         result += ">%s/%s: " % (str(iter_semester.year), str(iter_semester.semester))
    #         for iter_gradeSubject in iter_semester.subjects:
    #             result += "(%s,%s) " % (iter_gradeSubject.subject.code, iter_gradeSubject.subject.name)
    #     # l.info(result)
    #     return result.encode('utf-8')

    def __convert_solution_to_string(self, solution):
        result = ""
        for i in range(solution.member.num_studied_semester_id , len(solution.semesters)):
            iter_semester = solution.semesters[i]
            iter_semester.subjects.sort(key=lambda x: str(x.subject.id), reverse=False)
            result += "[%s/%s| " % (str(iter_semester.year), str(iter_semester.semester))
            # l.info("[%s/%s| " % (str(iter_semester.year), str(iter_semester.semester)))
            for iter_gradeSubject in iter_semester.subjects:
                # l.info("%s " % (iter_gradeSubject.subject.id))
                result += "%s " % (iter_gradeSubject.subject.id)
            result += ']'
        # l.info(result)
        return result.encode('utf-8')

    def __store_solution(self, solution):
        if len(self.tabu_list) == self.tabu_size:
            self.tabu_list.pop(0)
            l.info("Tabu is full. Removing oldest solution from Tabu List (size %d)" % (self.tabu_size))
        self.tabu_list.append(self.__generate_solution_id(solution))
        return True
