from r2als import scoring
import random
import hashlib

class Processor:

    # This is simple progress of Tabu Search

    workingSolution = None
    initialSolution = [9,8,7,6,5,4,3,2,1,0]
    bestSolution = None
    isWorking = True
    # TABU
    # tabuLists store hash of data
    tabuLists = []
    tabuSize = 20

    ################ tabu method ################

    def hashSolution(self, lists):
        strLists = ",".join(str(x) for x in lists)
        print(strLists)
        return hashlib.sha512(strLists).hexdigest()
    def addTabuLists(self, data):
        # hash data
        if len(self.tabuLists) <= self.tabuSize:
            self.tabuLists.append(self.hashSolution(data))
        else:
            self.tabuLists.popleft()
    def hasTabuLists(self, data):
        hashedData = self.hashSolution(data)
        for tabuList in self.tabuLists:
            if hashedData == tabuList:
                return True
        return False

    ################ scoring method ################

    def getScore(self, data):
        return scoring.calculate(data)
    def printScore(self, data):
        print("The score is "+str(self.getScore(data))+" : ", end=" ")
        print(data)

    ################ solution method ################

    def loadInitialSolution(self):
        return self.initialSolution

    def getNewSolution(self):
        random.shuffle(self.workingSolution)

    def compareScoreBestSolution(self):
        if scoring.calculate(self.workingSolution) > scoring.calculate(self.bestSolution):
            self.bestSolution = self.workingSolution

    def start(self):
        print("Started processor")
        self.workingSolution = self.loadInitialSolution()
        self.bestSolution = self.workingSolution
        self.printScore(self.workingSolution)

        while self.isWorking:
            self.getNewSolution()
            if self.hasTabuLists(self.workingSolution):
                # Ignore this solution
                continue
            else:
                self.addTabuLists(self.workingSolution)
            self.compareScoreBestSolution()

            if scoring.calculate(self.bestSolution) >= 8:
                self.isWorking = False
