#(2) p322. 10번에 다음 기능을 추가

from tkinter import *

## 전역변수 선언부
photo = None
x, y = None, None

## 함수 선언부

#확대하기 - 이벤트가 아님.
from tkinter.simpledialog import *
def zoomIn():
    global photo
    value = askinteger("확대배수", "확대할 배수를 입력하세요.(2~8)")
    photo = photo.zoom(value, value)
    pLabel.configure(image = photo)
    # pLabel.photo = photo => 확대, 축소에서는 필요 없음. Q. why?

#축소하기
def zoomOut():
    global photo
    value = askinteger("축소배수", "축소할 배수를 입력하세요.(2,8)")
    photo = photo.subsample(value, value)
    pLabel.configure(image = photo)

## 메인 코드부

if __name__ == "__main__":
    window = Tk()
    window.title("영화 감상하기")
    window.geometry("800x500")
    window.resizable(width = False, height = True)

    #이미지 보여주기
    photo = PhotoImage(file = "C:/images/Pet_GIF/Pet_GIF(256x256)/cat01_256.gif")
    pLabel = Label(window, image = photo)

    #메뉴 만들기
    mainMenu = Menu(window)
    window.config(menu = mainMenu)

    # '파일' 메뉴 만들기
    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "파일", menu=fileMenu)

    # '이미지 효과' 메뉴 만들기
    imageMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "이미지 효과", menu=imageMenu)
    imageMenu.add_command(label = "확대하기", command = zoomIn)
    imageMenu.add_command(label = "축소하기", command = zoomOut)

    #가운데 맞춤.
    pLabel.pack(expand=True)

    window.mainloop()


# 출처 : https://hashcode.co.kr/questions/7044/%ED%8C%8C%EC%9D%B4%EC%8D%AC-%EA%B7%B8%EB%A6%BC%ED%99%95%EB%8C%80
#- 확대, 축소 하는 코드 잘 나타나있음.