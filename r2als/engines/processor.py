# import copy
import random

from r2als.libs.solutions import InitialSolution, PreInitialSolution
from r2als.libs.snap_solution import SnapSolution
from r2als.libs.logs import Log
from r2als.engines.validator import validator
from r2als.engines.tabu_manager import TabuManager
from r2als.libs.next_solution_methods import *
from r2als.engines.scoring import Scoring

SEED = 47

l=Log("engine/Processor").getLogger()

class Processor:

    def __init__(self, member):
        self.result_solutions = []
        self.member = member
        self.high_score_is_good = False
        self.best_solution = None

    def start(self):
        l.info("Starting processor...")
        random.seed(SEED)
        tabu = TabuManager(20)
        working_solution = InitialSolution(self.member, random).get_solution()
        working_solution.score = Scoring(working_solution).get_score()
        self.best_solution = SnapSolution(working_solution)
        # self.__add_to_result(self.best_solution)
        validator(working_solution, ['*'])
        num_nsg_fail = 0
        num_validate_fail = 0
        num_add_tabu_fail = 0
        num_equal_best = 0

        for i in range(100):
            l.info("-"*45)
            l.info("Random "+str(i) + " rounds ....")
            tmp_solution = self.__next_solution_generator(working_solution)
            if tmp_solution is None:
                num_nsg_fail = num_nsg_fail + 1
                continue
            working_solution = tmp_solution
            if validator(working_solution, ['*']) is False:
                num_validate_fail = num_nsg_fail + 1
                break
            if not tabu.add_next_solution(working_solution):
                num_add_tabu_fail = num_add_tabu_fail + 1
                continue
            working_solution.score = Scoring(working_solution).get_score()
            l.info("Current score %d" %(working_solution.score))
            if self.__compare_best_solution(working_solution):
                num_equal_best = num_equal_best + 1
            if working_solution == self.best_solution:
                l.error("Something wrong")
                break
            l.warn("Adding to result %d" % (len(self.result_solutions)) )
            self.__add_to_result(SnapSolution(working_solution))
            if len(self.result_solutions) > 11:
                break
        # self.__add_to_result(self.best_solution)
        # self.__add_to_result(working_solution)
        l.info("Ended processor")
        l.info("-"*60)
        l.info("The result")
        l.info("-"*60)
        l.info("Random seed: " + str(SEED))
        l.info("Num of Next Solution Generator can't find the solution: " + str(num_nsg_fail))
        l.info("Num of solution which validate fail: " + str(num_validate_fail))
        l.info("Num of solution which exist in tabu: " + str(num_add_tabu_fail))
        l.info("Num of solution which has score equal to the best: " + str(num_equal_best))
        l.info("="*60)
        return self.result_solutions

    # def __prepare(self):
    #     l.info("Preparing some data....")
    #     solution = InitialSolution(self.member).get_solution()
    #     # tabu = TabuManager(20)
    #     # tabu.add_next_solution(solution)
    #     # self.result_solutions.append(solution)
    #     return solution

    def __compare_best_solution(self, solution):
        l.info("Comparing between best(%d), current(%d)" % (self.best_solution.score, solution.score))
        if self.high_score_is_good:
            if self.best_solution.score < solution.score:
                self.best_solution = SnapSolution(solution)
                l.warn("Best score is " + self.best_solution.score)
            elif self.best_solution.score == solution.score:
                l.info("Score is equal with the best")
                # self.__add_to_result(SnapSolution(solution), False)
                return True
        else:
            if self.best_solution.score > solution.score:
                self.best_solution = SnapSolution(solution)
                l.warn("Best score is " + self.best_solution.score)
            elif self.best_solution.score == solution.score:
                l.info("Score is equal with the best")
                return True
                # self.__add_to_result(SnapSolution(solution), False)
        l.info("After: Comparing between best(%d), current(%d)" % (self.best_solution.score, solution.score))
        return False
    def __add_to_result(self, solution, is_sort=True):
        self.result_solutions.append(solution)
        if is_sort:
            self.result_solutions.sort(key=lambda x: str(x.score), reverse=self.high_score_is_good)

    def __next_solution_generator(self, solution):
        tmp_solution = RandomSubjectWithRules(solution).get_solution(random)
        if tmp_solution is not None:
            solution = MoveWholeChain(solution).get_solution()
            solution = MoveNonRelatedSubjectOut(solution).get_solution(random)
            solution.get_ready()
            # solution.update_all_prerequisite()
            return solution
        return None
