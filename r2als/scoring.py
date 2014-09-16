

def calculate(data):
    totalScore = 0
    # for i in reversed(range(1,len(data))):
    i = len(data) - 1
    while i > 0 :
        if data[i-1] < data[i]:
            totalScore += 1
        i -= 1
    return totalScore
