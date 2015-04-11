# import copy
import random

from r2als.libs.solutions import InitialSolution, PreInitialSolution
from r2als.libs.snap_solution import SnapSolution
from r2als.libs.logs import Log
from r2als.engines.validator import validator
from r2als.engines.tabu_manager import TabuManager
from r2als.libs.next_solution_methods import *
from r2als.engines.scoring import Scoring
from r2als.engines.filter import Filter

l=Log("engine/Processor").getLogger()

class Processor:

    def __init__(self, member, tabu_size, target_num_solution, seed=None):
        self.result_solutions = []
        self.member = member
        self.tabu_size = tabu_size
        self.high_score_is_good = False
        self.best_solution = None
        self.seed = seed
        self.target_num_solution = target_num_solution

        self.num_nsg_fail = 0
        self.num_validate_fail = 0
        self.num_add_tabu_fail = 0
        self.num_equal_best = 0
        self.num_iteration = 1

    def start(self):
        l.info("Starting processor...")
        random.seed(self.seed)
        tabu = TabuManager(self.tabu_size)
        # tmp_solution = PreInitialSolution(self.member).get_solution()
        # tmp_solution.score = Scoring(tmp_solution).get_score()
        # self.__add_to_result(SnapSolution(tmp_solution), False)
        working_solution = InitialSolution(self.member, random).get_solution()
        working_solution.score = Scoring(working_solution).get_score()
        self.best_solution = SnapSolution(working_solution)
        # self.__add_to_result(self.best_solution, False)
        validator(working_solution, ['*'])

        self.num_iteration=1
        while True:
            l.info("-"*45)
            l.info("Random "+str(self.num_iteration) + " rounds ....")
            self.num_iteration+=1
            tmp_solution = self.__next_solution_generator(working_solution)
            if tmp_solution is None:
                self.num_nsg_fail = self.num_nsg_fail + 1
                continue
            working_solution = tmp_solution
            if validator(working_solution, ['*']) is False:
                self.num_validate_fail = self.num_nsg_fail + 1
                break
            if not tabu.add_next_solution(working_solution):
                self.num_add_tabu_fail = self.num_add_tabu_fail + 1
                continue
            working_solution.score = Scoring(working_solution).get_score()
            l.info("Current score %d" %(working_solution.score))
            if self.__compare_best_solution(working_solution):
                self.num_equal_best = self.num_equal_best + 1
            if working_solution == self.best_solution:
                l.error("Something wrong")
                break
            l.info("Adding to result %d" % (len(self.result_solutions)) )
            self.__add_to_result(SnapSolution(working_solution))
            if len(self.result_solutions) == self.target_num_solution:
                break

        # self.__add_to_result(self.best_solution)
        # self.__add_to_result(working_solution)
        l.info("Ended processor")
        l.info("-"*60)
        l.info("The result")
        l.info("-"*60)
        for extra in self.conclusion_list():
            l.info(extra)
        l.info("="*60)
        return self.result_solutions
        # return Filter(self.result_solutions, extras).start()

    # def __prepare(self):
    #     l.info("Preparing some data....")
    #     solution = InitialSolution(self.member).get_solution()
    #     # tabu = TabuManager(20)
    #     # tabu.add_next_solution(solution)
    #     # self.result_solutions.append(solution)
    #     return solution

    def conclusion_list(self):
        extras = []
        extras.append("Random seed: " + str(self.seed))
        extras.append("Num of iteration: "+ str(self.num_iteration))
        extras.append("Num of Next Solution Generator can't find the solution: %d (%.2f%s)" % (self.num_nsg_fail, float(self.num_nsg_fail/self.num_iteration*100),'%'))
        extras.append("Num of solution which validate fail: %d (%.2f%s)" % (self.num_validate_fail, float(self.num_validate_fail/self.num_iteration*100),'%'))
        extras.append("Num of solution which exist in tabu: %d (%.2f%s)" % (self.num_add_tabu_fail, float(self.num_add_tabu_fail/self.num_iteration*100),'%'))
        extras.append("Num of solution which has score equal to the best: %d (%.2f%s)" % (self.num_equal_best, float(self.num_equal_best/self.num_iteration*100),'%'))
        return extras

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
        # tmp_solution = RandomSubjectWithRules(solution).get_solution_move_only(random)
        if tmp_solution is not None:
            solution = MoveWholeChain(solution).get_solution()
            solution = MoveNonRelatedSubjectOut(solution).get_solution(random)
            solution.get_ready()
            # solution.update_all_prerequisite()
            return solution
        return None
