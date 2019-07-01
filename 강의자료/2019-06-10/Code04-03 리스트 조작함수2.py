## 특정값의 모든 위치를 출력하는 프로그램
import random
myList = [random.randint(1,5) for _ in range(10)]
print(myList)
NUMBERS = 5
index = 0
for i in range(myList.count(NUMBERS)):    # NUMBERS의 갯수 찾기.
    index = myList.index(NUMBERS, index)
    print(index)
    index += 1
#설명
##과정
# myList => [2, 4, 5, 3, 5, 2, 5, 4, 2, 1] 라고 했을 때
# 1. myList.index(5,0)을 하면 처음 나오는 5의 인덱스를 찾는다.
#   즉, target이 5가 되고, 0부터 찾기 시작한다. => 인덱스 값이 2
# 2. index +=1 을 해줘야 처음 나오는 5 다음 값부터 5를 찾게 된다. => 인덱스 값이 4
# 3. index +=1 을 해줘야 처음 나오는 5 다음 값부터 5를 찾게 된다. => 인덱스 값이 6
# 다음 실행하면 error가 뜨는데, for문에서는 myList.count(5)를 하면 값이 3이기 때문에, 딱 세 번만 실행하게 된다.

