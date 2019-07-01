## Selection Sort ##

import random
dataList = [random.randint(1,99) for _ in range(20) ]
print(dataList)

# for i in range(0, len(dataList) - 1):
#     for k in range(i+1, len(dataList)):
#         if dataList[i] > dataList[k]:
#             dataList[i], dataList[k] = dataList[k], dataList[i]
#             # temp = dataList[i]
#             # dataList[i] = dataList[k]
#             # dataList[k] = temp
# print(dataList)

## Bubble Sort ##
for i in range(0, len(dataList) - 1):
    change = False
    for k in range(0, len(dataList) - 1 - i): # 끝에부터 정렬이 되므로, i 개만큼 감소함.
        if dataList[k] > dataList[k+1]:
            dataList[k], dataList[k+1] = dataList[k+1], dataList[k]
            change = True
    if change == False:   # change = False 로 둔 이유는 break-point로 잡아, 빠르게 끝내기 위함.
        break
print(dataList)
