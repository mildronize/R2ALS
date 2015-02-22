# import copy
from r2als.libs.solutions import InitialSolution
from r2als.libs.snap_solution import SnapSolution
from r2als.libs.logs import Log
from r2als.engines.validator import validator
from r2als.engines.tabu_manager import TabuManager
from r2als.libs.next_solution_methods import *
from r2als.engines.scoring import Scoring


l=Log("engine/Processor").getLogger()

class Processor:

    def __init__(self, member):
        self.result_solutions = []
        self.member = member
        self.high_score_is_good = False
        self.best_solution = None

    def start(self):
        l.info("Starting processor...")

        tabu = TabuManager(20)
        current_solution = InitialSolution(self.member).get_solution()
        current_solution.score = Scoring(current_solution).get_score()
        self.best_solution = SnapSolution(current_solution)

        for i in range(30):
            l.info("-"*45)
            l.info("Random "+str(i) + " rounds ....")
            tmp_solution = self.__next_solution_generator(current_solution)
            if tmp_solution is None:
                continue
            current_solution = tmp_solution
            if validator(current_solution, ['*']) is False:
                continue
            if not tabu.add_next_solution(current_solution):
                continue
            current_solution.score = Scoring(current_solution).get_score()
            l.warn("Current score %d" %(current_solution.score))
            # if self.best_solution is None:
            #     self.best_solution = SnapSolution(current_solution).get()
            # else:
            self.__compare_best_solution(current_solution)

            if current_solution == self.best_solution:
                l.error("Something wrong")
                break
        self.__add_to_result(self.best_solution)
        l.info("Ended processor")
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
        else:
            if self.best_solution.score > solution.score:
                self.best_solution = SnapSolution(solution)
                l.warn("Best score is " + self.best_solution.score)
            elif self.best_solution.score == solution.score:
                l.info("Score is equal with the best")
        l.warn("After: Comparing between best(%d), current(%d)" % (self.best_solution.score, solution.score))

    def __add_to_result(self, solution):
        self.result_solutions.append(solution)
        self.result_solutions.sort(key=lambda x: str(x.score), reverse=self.high_score_is_good)

    def __next_solution_generator(self, solution):
        tmp_solution = RandomSubjectWithRules(solution).get_solution()
        if tmp_solution is not None:
            solution = MoveWholeChain(solution).get_solution()
            solution.get_ready()
            return solution
        return None



