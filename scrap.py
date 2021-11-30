class testing(object):
    def __init__(self, attribute):
        self.manualAttribute = attribute
        self.autoAttribute = True
    

testSet = set()


testing1 = testing("testing")

testSet.add(testing1)

testing1 = testing("testing")

testSet.add(testing1)

print(testSet)

print(list(testSet))

print(list(testSet)[0] == list(testSet)[1])
