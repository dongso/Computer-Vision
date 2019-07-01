def func1():
    global a
    a = 10
    print('func1() --> ', a)

def func2():
    global a
    print('func2() --> ', a )

## 변수 선언부
a = 1234

## 메인 코드부
func1()
print(a) #a가 10으로 변경되어 있기를 기대함.
func2()


