# 퀴즈2에 메뉴를 추가하자.
#[이동] >> [앞으로], [뒤로]
#[건너뛰기] >> [1], [3], [5]
from tkinter import *

## 전역변수 선언부 ##
dirName = "C:/images/Pet_GIF/Pet_GIF(256x256)/"
fnameList = ["cat01_256.gif","cat02_256.gif","cat03_256.gif",
             "cat04_256.gif","cat05_256.gif","cat06_256.gif"]

photoList = [None] * 6
num = 0 # 현재 사진 순번

## 함수 선언부
def clickPrev():
    global num
    num -= 1
    if num < 0:
        num = len(fnameList) - 1
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image=photo)
    label1.configure(text=fnameList[num])
    pLabel.photo = photo

def clickNext():
    global num
    num += 1
    if num >= len(fnameList):
        num = 0
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image=photo)
    label1.configure(text=fnameList[num])
    ##configure()는 기존 것 있고, 속성만 바꿔줌.
    pLabel.photo = photo

def homePress(event):
    global num
    num = 0
    photo = PhotoImage(file =dirName + fnameList[num])
    pLabel.configure(image = photo)
    label1.configure(text=fnameList[num])
    pLabel.photo = photo
    #pName = fnameList[num]

def endPress(event):
    global num
    num = len(fnameList) -1
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image = photo)
    label1.configure(text=fnameList[num])
    pLabel.photo = photo

def rightPress(event):
    global num
    num += 1
    if num > len(fnameList)-1:
        num = 0
    photo = PhotoImage(file=dirName + fnameList[num])
    pLabel.configure(image = photo)
    label1.configure(text=fnameList[num])
    pLabel.photo = photo

def leftPress(event):
    global num
    num -= 1
    if num < 0:
        num = len(fnameList) -1
    photo = PhotoImage(file = dirName + fnameList[num])
    pLabel.configure(image = photo)
    label1.configure(text=fnameList[num])
    pLabel.photo = photo

def numPress(event):
    string = chr(event.keycode)
    num = int(string) -1
    if num > len(fnameList) - 1:
        num = len(fnameList) - 1
    photo = PhotoImage(file = dirName + fnameList[num])
    pLabel.configure(image = photo)
    label1.configure(text=fnameList[num])
    pLabel.photo = photo


from tkinter.simpledialog import *
def hopImage(count = 0):
    if count == 0:
        count = askinteger("건너뛸 수", "숫자~~~~>")
    for _ in range(count):
        clickNext()

# #건너뛰기 함수
# def hopImage(x):
#     global num
#     num = (num +x) % len(fnameList)

from tkinter.filedialog import *
def selectFile():
    filename = askopenfilename(parent = window,
                               filetypes=(("GIF파일", "*.gif;*.raw"), ("모든파일", "*.*")))
    print(filename)
    pLabel.configure(text = str(filename))
    pLabel.text = filename



## 메인 코드부
window = Tk()
window.title("GIF 사진 뷰어 (Ver 0.01)")
window.geometry("500x300")
window.resizable(width =False, height = True)

photo = PhotoImage(file = dirName + fnameList[num])
pLabel = Label(window, image = photo)

btnPrev = Button(window, text = '<< 이전', command = clickPrev)
label1 = Label(window, text=fnameList[num])
btnNext = Button(window, text = '다음>>', command = clickNext)

#Home 버튼 -> 첫그림
window.bind("<Home>", homePress)

#End 버튼 -> 마지막그림
window.bind("<End>", endPress)

#-> 버튼 --> 다음그림
window.bind("<Right>", rightPress)

#<- 버튼 --> 이전그림
window.bind("<Left>", leftPress)

#숫자는 현재그림 + 숫자위치 : 넘기면 마지막그림
window.bind("<Key>", numPress)

#메뉴 만들기
mainMenu = Menu(window)
window.config(menu = mainMenu)

#이동
fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "이동", menu = fileMenu)
fileMenu.add_command(label = "앞으로", command=clickPrev)
fileMenu.add_command(label = "뒤로", command=clickNext)

#건너뛰기 - fileMenu를 하나 더 만들면 초기화가 되더라구...
hopMenu = Menu(mainMenu)
mainMenu.add_cascade(label = "건너뛰기", menu = hopMenu)
# for i in range(len(fnameList)):
#     string = chr(i+)
#     fileMenu.add_command(label = string, command = lambda : hopImage(i))
hopMenu.add_command(label = "1", command = lambda : hopImage(1))
hopMenu.add_command(label = "3", command = lambda : hopImage(3))
hopMenu.add_command(label = "5", command = lambda : hopImage(5))
hopMenu.add_command(label = "원하는 수 ", command = lambda : hopImage())
hopMenu.add_separator()
hopMenu.add_command(label = "Select File", command = selectFile)

btnPrev.place(x=130, y=10); label1.place(x=200, y=10); btnNext.place(x=300, y=10)
pLabel.place(x=15, y = 50)
window.mainloop()