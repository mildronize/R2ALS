

class Processor:

    # This is simple progress of Tabu Search
    workingSolution = None
    initialSolution = range(10)

    def loadInitialSolution(self):
        return self.initialSolution

    def start(self):
        print("Started processor")
        workingSolution = self.loadInitialSolution()
        for s in workingSolution:
            print(s)

