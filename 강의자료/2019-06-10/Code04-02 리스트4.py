#4일차
# 퀴즈1. 10크기의 영상 데이터를 랜덤하게 준비한 후, 영상에 밝기를 더한다. (10을 더하기)
#출력은 원영상, 밝아진 영상

## 빈 메모리를 확보한 후에, 작업하기
import random
SIZE = 10
## 1. 메모리 확보 개념(타 언어 스타일) ##
aa = [] # 빈 리스트 준비
for i in range(SIZE):
    aa.append(0)

## 2. 메모리에 필요한 값 대입 --> 파일 읽기
for i in range(SIZE): # range(0,4,1)
    num = random.randint(0,99)
    aa[i] = num
print('원 영상 -->', aa)
## 3. 메모리 처리/조작/연산~~~~ --> 알고리즘(컴퓨터 비전, 영상처리)
sum = 0
for i in range(SIZE):
    aa[i] += 10
    if aa[i] > 99 :  # overflow 발생 대비
        aa[i] = 99
## 4. 출력
print('영상 평균값 --> ', aa)