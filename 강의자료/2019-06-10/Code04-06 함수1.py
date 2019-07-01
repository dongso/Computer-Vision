## 두 수를 받아서 더한 값을 반환하는 함수
def plus(v1, v2):
    result = 0
    result = v1 + v2
    return result

## 두 수를 받아서 더한 값을 반환하는 함수
def calc(v1, v2=0):
    result1 = v1 + v2
    result2 = v1 - v2
    return result1, result2

def calc2(*para):
    res = 0
    for num in para:
        res += num
    return res

## 메인 코드붐
hap1, hap2 = calc(100)
hap = calc2(12,3,3,4,5,6,7)
print(hap)

## 메인 코드부
hap = plus(100,200)
print(hap)

hap = plus(200,300)
print(hap)

hap = plus(300,400)
print(hap)

