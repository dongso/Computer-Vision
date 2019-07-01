# def outFunc(v1, v2):
#     def inFunc(n1, n2):
#         return n1 * n2
#     return inFunc(v1, v2)
#
# print(outFunc(100,200))
#
# def hap(v1, v2):
#     res = v1 + v2
#     return res
#
# hap2 = lambda v1, v2 : v1 + v2
#
# print(hap(100,200))
# print(hap2(100,200))

myList = [1,2,3,4,5]
# def add10(num):
#    return num + 10
# add10 = lambda num : num + 10
# for i in range(len(myList)):
#     myList[i] = add10(myList[i])
#myList = list(map(add10, myList) 에서 밑과 같이 변형됨.
myList = list(map(lambda num : num + 10, myList))

print(myList)

