from r2als import scoring
import random
import hashlib
import copy

class Processor:

    # This is simple progress of Tabu Search

    workingSolution = None
    initialSolution = [9,8,7,6,5,4,3,2,1,0]
    bestSolution = None
    isWorking = True
    # TABU
    # tabuLists store hash of data
    tabuLists = []
    tabuSize = 0

    def __init__(self, tabuSize=None):
        if tabuSize is None:
            self.tabuSize = 20
        else:
             self.tabuSize = tabuSize

    ################ tabu method ################
    def convertList2String(self, lists):
        strLists =   ",".join(str(x) for x in lists)
        strLists_bytes = strLists.encode('utf-8')
        return strLists_bytes
    def hashSolution(self, lists):
        return hashlib.sha256(self.convertList2String(lists)).hexdigest()

    def addTabuLists(self, data):
        # hash data
        if len(self.tabuLists) <= self.tabuSize:
            self.tabuLists.append(self.hashSolution(data))
        else:
            self.tabuLists.pop(0)
    def hasTabuLists(self, data):
        hashedData = self.hashSolution(data)
        for tabuList in self.tabuLists:
            if hashedData == tabuList:
                return True
        return False

    ################ scoring method ################

    def getScore(self, lists):
        return scoring.calculate(lists)
    def printScore(self, lists):
        print("The score is "+str(self.getScore(lists))+" : ", end=" ")
        print(lists)

    ################ solution method ################

    def loadInitialSolution(self):
        return self.initialSolution

    def getNewSolution(self):
        random.shuffle(self.workingSolution)

    def compareScoreBestSolution(self):
        #print("compareScoreBestSolution!")
        if scoring.calculate(self.workingSolution) > scoring.calculate(self.bestSolution):
            print("Get best solution!")
            self.bestSolution = copy.copy(self.workingSolution)
            self.printScore(self.bestSolution)

    def start(self):
        print("Starting processor")
        self.workingSolution = self.loadInitialSolution()
        self.bestSolution = copy.copy(self.workingSolution)
        # print(type(self.workingSolution))
        # print(type(self.bestSolution))
        self.printScore(self.workingSolution)

        while self.isWorking:
            self.getNewSolution()
            if self.hasTabuLists(self.workingSolution):
                # Ignore this solution
                continue
            else:
                self.addTabuLists(self.workingSolution)
            self.compareScoreBestSolution()
            # print("########################")
            # print("best")
            # self.printScore(self.bestSolution)
            # print("working")
            # self.printScore(self.workingSolution)
            # input("Press to continue")
            if scoring.calculate(self.bestSolution) >= 8:
                self.isWorking = False

        print("End processor")
