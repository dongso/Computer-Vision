from tkinter import *

## 전역변수 선언부 ##
dirName = "C:/images/Pet_GIF/Pet_GIF(256x256)/"
fnameList = ["cat01_256.gif","cat02_256.gif","cat03_256.gif",
             "cat04_256.gif","cat05_256.gif","cat06_256.gif"]
photoList = [None] * 6
num = 0 # 현재 사진 순번
## 함수 선언부
def clickPrev():
    pass

def clickNext():
    global num
    num +=1
    if num >= len(fnameList):
        num = 0
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image= photo)
    ##configure()는 기존 것 있고, 속성만 바꿔줌.
    pLabel.photo = photo

## 메인 코드부
window = Tk()
window.title("GIF 사진 뷰어 (Ver 0.01)")
window.geometry("500x300")
window.resizable(width =False, height = True)

photo = PhotoImage(file = dirName + fnameList[num])
pLabel = Label(window, image = photo)

btnPrev = Button(window, text = '<< 이전 그림', command = clickPrev)
btnNext = Button(window, text = '다음 그림>>', command = clickNext)

btnPrev.place(x=150, y=10); btnNext.place(x=250, y=10)
pLabel.place(x=15, y = 50)
window.mainloop()