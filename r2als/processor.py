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

    def __init__(self, tabuSize=20):
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
        #random.shuffle(self.workingSolution)
        firstPointer = random.randint(1, len(self.initialSolution)) - 1
        while True:
            secondPointer = random.randint(1, len(self.initialSolution)) - 1
            if secondPointer != firstPointer:
                break
        self.workingSolution[firstPointer], self.workingSolution[secondPointer] = self.workingSolution[secondPointer], self.workingSolution[firstPointer]

    def compareScoreBestSolution(self):
        #print("compareScoreBestSolution!")
        if scoring.calculate(self.workingSolution) > scoring.calculate(self.bestSolution):
            print("Working Solution ", end=" ")
            self.printScore(self.workingSolution)
            print("Old best Solution", end=" ")
            self.printScore(self.bestSolution)
            self.bestSolution = copy.copy(self.workingSolution)
            print("--> best Solution",end=" ")
            self.printScore(self.bestSolution)
            print("#"*100)

    def start(self):
        print("Starting processor")
        self.workingSolution = self.loadInitialSolution()
        self.bestSolution = copy.copy(self.workingSolution)
        self.printScore(self.workingSolution)

        print("#"*100)

        while self.isWorking:
            self.getNewSolution()
            if self.hasTabuLists(self.workingSolution):
                continue
            else:
                self.addTabuLists(self.workingSolution)
            self.compareScoreBestSolution()

            if scoring.calculate(self.bestSolution) >= 8:
                self.isWorking = False

        print("End processor")
