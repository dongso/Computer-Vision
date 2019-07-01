from tkinter import *

class Car: # 자동차 설계도
    # 자동차 속성
    color = None
    speed = 0
    # 자동차의 행위(---> 함수, 기능)
    def upSpeed(self, value):
        # speed = 0    # speed는 변수
        self.speed += value # speed는 속성. 따라서 self.speed로 표현해야 함.
    def downSpeed(self, value):
        self.speed -= value

###########################
myvalue = 0
car1 = Car(); car2 = Car()

car1.color = "빨강"
car1.speed = 50
car1.upSpeed(100)
print(car1.color)
print(car1.speed)

car2.color = "파랑"
car2.speed = 100
car2.upSpeed(200)
print(car2.color)
print(car2.speed)

# button1 = Button().invoke()
# Button() 클래스임 / button1은 인스턴스 / invoke()는 Button 클래스 안에 있는 메서드
