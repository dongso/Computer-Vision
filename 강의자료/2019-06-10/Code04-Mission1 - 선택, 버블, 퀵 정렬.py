#  1. 선택 정렬

#  2. 버블정렬
# 인접한 2개의 레코드를 비교하여 크기가 순서대로 되어있지 않으면
# 서로 교환하는 비교-교환 과정을 리스트의 왼쪽 끝에서 시작하여 오른쪽
# 끝까지 진행. => 스캔 과정이 이루어짐.

#  3. 퀵 정렬
#-분할 정복 알고리즘의 하나로, 평균적으로 매우 빠른 수행 속도를 자랑함.
#-리스트를 비균등하게 분할
#-분할 정복 방법
#문제를 작은 2개의 문제로 분리하고 각각을 해결한 다음, 결과를 모아서 원래의 문제를 해결
#순환 호출을 이용하여 구현.
#-과정 설명
#1.리스트 안에 있는 한 요소 선택. => 고른 원소를 피벗(pivot)이라고 함.
#2.피벗을 기준으로 피벗보다 작은 요소들은 모두 피벗의 왼쪽으로 옮겨지고
#피벗보다 큰 요소들은 모두 피벗의 오른쪽으로 옮겨짐.
#3.피벗을 제외한 왼쪽 리스트와 오른쪽 리스트를 다시 정렬한다.
#분할된 부분 리스트에 대하여 순환 호출을 이용하여 정렬을 반복.
#부분 리스트에서도 다시 피벗을 정하고 피벗을 기준으로 2개의 부분 리스트로 나누는 과정 반복.
#4. 부분 리스트들이 더 이상 분할이 불가능할 때까지 반복.

#선택정렬
def selection_sort(data):
    for i in range(len(data)-1, 0, -1):
        for k in range(0, i):
            if(data[k] > data[k+1]):
                temp = data[k]
                data[k] = data[k+1]
                data[k+1] = temp
    print("selection 정렬 후 데이터 : ", end='')
    [print(num, end=' ') for num in data]
#버블정렬
def bubble_sort(data):
    for i in range(len(data)-1, 0, -1):
        for k in range(0, i):
            if(data[k] > data[k+1]):
                temp = data[k]
                data[k] = data[k+1]
                data[k+1] = temp
    print("bubble 정렬 후 데이터 : ", end='')
    [print(num, end=' ') for num in data]
#퀵정렬
def quick_sort(data):
    total_sorted = []
    if len(data) <= 1:
        return data
    pivot = data[len(data) // 2]
    lesser_arr, equal_arr, greater_arr = [], [], []
    for num in data:
        if num < pivot:
            lesser_arr.append(num)
        elif num > pivot:
            greater_arr.append(num)
        else:
            equal_arr.append(num)
    return quick_sort(lesser_arr) + equal_arr + quick_sort(greater_arr)

# 공통 -> 메인 부분
# (1) p.219 16진수 정렬
import random

data = []

print("------------16진수 정렬----------------------------")
if __name__ == "__main__":
    for i in range(5):
        temp = hex(random.randrange(0,10000))
        data.append(temp)
    print("정렬 전 데이터 : ", end='')
    [print(num, end=' ') for num in data]
    print()
    #selection_sort
    selection_sort(data)
    print()
    #bubble_sort
    bubble_sort(data)
    print()
    #quick_sort
    data = quick_sort(data)
    print("quick 정렬 후 데이터 : ", end='')
    [print(num, end=' ') for num in data]
print()

# (2) p.283 문자, 숫자 정렬
import random

data = []
print("------------문자, 숫자 정렬---------------------------")
## 메인 코드 부분 ##
if __name__ == "__main__":
    for i in range(5):
        temp = hex(random.randrange(0, 10000))
        temp = temp[2:]
        data.append(temp)
    print("정렬 전 데이터 : ", end='')
    [print(num, end=' ') for num in data]
    print()
    # selection_sort
    selection_sort(data)
    print()
    # bubble_sort
    bubble_sort(data)
    print()
    # quick_sort
    data = quick_sort(data)
    print("quick 정렬 후 데이터 : ", end='')
    [print(num, end=' ') for num in data]
