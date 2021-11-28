# from datetime import *
# test = datetime(2021, 11, 11, 16, 15, tzinfo=None)
# print(test.year)


def interleaveListHelper(dictOfLists):
    someEmpty = False
    emptyLists = {}
    for l in dictOfLists:
        if len(dictOfLists[l]) == 0:
            someEmpty = True
            emptyLists[l] = dictOfLists[l]
    nonEmptyDict = {n:l for n,l in dictOfLists.items() if n not in emptyLists}
    if someEmpty:
        return interleaveListHelper(nonEmptyDict)
    elif len(nonEmptyDict) == 1:
        for key in nonEmptyDict:
            return nonEmptyDict[key]
    else:
        interleavingList = []
        newDictOfLists = dict()
        for l in dictOfLists:
            interleavingList.append(dictOfLists[l][0])
            newDictOfLists[l] = dictOfLists[l][1:]
        interleavingList += interleaveListHelper(newDictOfLists)
        return interleavingList

dictOfLists = {"w" : ["1","2","3","4","5","6"],
              "x" : ["a","b","c","d","e","f"],
              "y" : ["_1","_2","_3","_4","_5","_6","_7","_8"],
              "z" : ["_a","_b","_c","_d","_e","_f", "_g", "_h", "_i","_j"]}
print(interleaveListHelper(dictOfLists))