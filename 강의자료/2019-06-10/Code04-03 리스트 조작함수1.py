## 특정값의 모든 위치를 출력하는 프로그램
import random
myList = [random.randint(1,5) for _ in range(10)]
print(myList)
NUMBERS = 5
index = 0
findList = []
#try, except 잘 활용.
while True :
    try:
        index = myList.index(NUMBERS, index)
        print(index)
        index += 1
    except:
        break
