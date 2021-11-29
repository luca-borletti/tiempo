# # from datetime import *
# # test = datetime(2021, 11, 11, 16, 15, tzinfo=None)
# # print(test.year)


# def interleaveListHelper(dictOfLists):
#     someEmpty = False
#     emptyLists = {}
#     for l in dictOfLists:
#         if len(dictOfLists[l]) == 0:
#             someEmpty = True
#             emptyLists[l] = dictOfLists[l]
#     nonEmptyDict = {n:l for n,l in dictOfLists.items() if n not in emptyLists}
#     if someEmpty:
#         return interleaveListHelper(nonEmptyDict)
#     elif len(nonEmptyDict) == 1:
#         for key in nonEmptyDict:
#             return nonEmptyDict[key]
#     else:
#         interleavingList = []
#         newDictOfLists = dict()
#         for l in dictOfLists:
#             interleavingList.append(dictOfLists[l][0])
#             newDictOfLists[l] = dictOfLists[l][1:]
#         interleavingList += interleaveListHelper(newDictOfLists)
#         return interleavingList

# dictOfLists = {"w" : ["1","2","3","4","5","6"],
#               "x" : ["a","b","c","d","e","f"],
#               "y" : ["_1","_2","_3","_4","_5","_6","_7","_8"],
#               "z" : ["_a","_b","_c","_d","_e","_f", "_g", "_h", "_i","_j"]}
# print(interleaveListHelper(dictOfLists))

hwAverage = 100.1      # This is the number you see in autolab
quizAverage = 86.6       # The number in autolab will change a tiny bit because of TP1/TP2
midtermAverage = 98.7    # This is the number you see in autolab
final = midtermAverage # Can replace with a hypothetical final exam score or keep as the midterm average
tp = 90                # Replace with a hypothetical TP score

grade = (0.3 * hwAverage) + (0.1 * quizAverage) + (0.2 * midtermAverage) + (0.2 * final) + (0.2 * tp)

if grade >= 89.5:
    print("A", grade)
elif grade >= 79.5:
    print("B", grade)
elif grade >= 69.5:
    print("C", grade)
elif grade >= 59.5:
    print("D", grade)
else:
    print("R", grade)


# print(max([3,2,11,2,55]))

print({15,10} - {20,15})