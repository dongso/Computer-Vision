#(1) p325. 그림판 만들기
#- 메뉴에 [도형] >> [선], [원]을 추가한 후 선을 선택하면 선이 그려지고, 원을 선택하면 원이 그려지기
from tkinter import *
import turtle

## 함수 선언 부분 ##

def lineClick(event):
    global x1, y1
    x1 = event.x
    y1 = event.y

def lineDrop(event):
    global x2, y2, penWidth, penColor
    x2 = event.x
    y2 = event.y
    canvas.create_line(x1, y1, x2, y2, width=penWidth, fill=penColor)

def circleClick(event):
    global x1, y1
    x1 = event.x
    y1 = event.y

def circleDrop(event):
    global x2, y2, penWidth, penColor
    x2 = event.x
    y2 = event.y
    canvas.create_oval(x1, y1, x2, y2, width=penWidth, fill=penColor, outline=penOutColor)

def drawLine():
    window.bind("<Button-1>", lineClick)
    window.bind("<ButtonRelease-1>", lineDrop)

def drawCircle():
    window.bind("<Button-1>", circleClick)
    window.bind("<ButtonRelease-1>", circleDrop)

## 전역 변수 선언 부분 ##
window = None
canvas = None
x1, y1, x2, y2 = None,None,None,None  # 선의 시작점과 끝점
penColor = 'blue'
penOutColor = 'red'
penWidth = 10

## 메인 코드 부분 ##
if __name__ == "__main__":
    window = Tk()
    window.title("재정이의 그림판")
    # 창의 크기 조절, Canvas가 그림판 역할을 함.
    canvas = Canvas(window, height = 300, width = 300)

    mainMenu = Menu(window)
    window.config(menu = mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "도형", menu = fileMenu)
    fileMenu.add_command(label = "선", command = drawLine)
    fileMenu.add_command(label = "원", command = drawCircle)

    canvas.pack()

    window.mainloop()