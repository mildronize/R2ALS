import random
import hashlib
import copy
from r2als import config
from r2als import models
# from r2als import scoring
from r2als.libs.solutions import InitialSolution
from r2als.libs.logs import Log

l=Log("engine/Processor").getLogger()

class Processor:

    def __init__(self, member):
        self.result_solutions = []
        self.member = member

    def start(self):
        l.info("Starting processor...")

        self.prepare()

        l.info("Ended processor")
        return self.result_solutions

    def prepare(self):
        l.info("Preparing some data....")
        solution = InitialSolution(self.member).get_solution()
        self.result_solutions.append(solution)



