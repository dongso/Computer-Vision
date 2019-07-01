# i, k = 0, 0

# for i in range(2,10,1):
#     print("## %d 단 ##" %(i))
#     for k in range(1,10,1):
#         print(i,'*',k,'=',i*k)

## 10 x 10 크기의 숫자를 예쁘게 출력하라 ##
import random
import random as rd
from random import randrange, randint # randrange를 바로 사용하겠다.
from random import *
##위 4가지 방식 사용.
#count = 0
for _ in range(10):
    for _ in range(10):
        num = randint(0,99) # randint(0,99) / 0~98까지 정수 랜덤 값.
        print("%2d " %(num), end='')  # %d가 아닌 %2d로 하면 숫자를 2칸으로 채우기 때문에 더 아름답게 만들어짐.
        #count += 1
    print()
