# 퀴즈2에 메뉴를 추가하자.
#[이동] >> [앞으로], [뒤로]
#[건너뛰기] >> [1], [3], [5]
from tkinter import *

## 전역변수 선언부 ##
#dirName = "C:/images/Pet_GIF/Pet_GIF(256x256)/"
#fnameList = ["cat01_256.gif","cat02_256.gif","cat03_256.gif",
#             "cat04_256.gif","cat05_256.gif","cat06_256.gif"]
fnameList = []
import os

photoList = [None] * 6
num = 0 # 현재 사진 순번

## 함수 선언부
def clickPrev():
    global num
    num -= 1
    if num < 0:
        num = len(fnameList) - 1
    photo = PhotoImage(file=fnameList[num])
    ##마지막 이미지의 '값' 형태로 불러오고,
    pLabel.configure(image=photo)
    ##pLabel에서 값을 구성하자.
    pLabel.photo = photo
    ##pLabel에서 사진을 가져오자...
    label1.configure(text=fnameList[num])

def clickNext():
    global num
    num += 1
    if num >= len(fnameList):
        num = 0
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image=photo)
    pLabel.photo = photo
    label1.configure(text=fnameList[num])
    ##configure()는 기존 것 있고, 속성만 바꿔줌.

def homePress(event):
    global num
    num = 0
    photo = PhotoImage(file =fnameList[num])
    pLabel.configure(image = photo)
    pLabel.photo = photo
    #pName = fnameList[num]
    label1.configure(text=fnameList[num])

def endPress(event):
    global num
    num = len(fnameList) -1
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image = photo)
    pLabel.photo = photo
    label1.configure(text=fnameList[num])

def rightPress(event):
    global num
    num += 1
    if num > len(fnameList)-1:
        num = 0
    photo = PhotoImage(file=fnameList[num])
    pLabel.configure(image = photo)
    pLabel.photo = photo
    label1.configure(text=fnameList[num])

def leftPress(event):
    global num
    num -= 1
    if num < 0:
        num = len(fnameList) -1
    photo = PhotoImage(file = fnameList[num])
    pLabel.configure(image = photo)
    pLabel.photo = photo
    label1.configure(text=fnameList[num])

def numPress(event):
    string = chr(event.keycode)
    num = int(string) -1
    if num > len(fnameList) - 1:
        num = len(fnameList) - 1
    photo = PhotoImage(file = fnameList[num])
    pLabel.configure(image = photo)
    pLabel.photo = photo
    label1.configure(text=fnameList[num])


from tkinter.simpledialog import *
def hopImage(count = 0):
    if count == 0:
        count = askinteger("건너뛸 수", "숫자~~~~>")
    ## default가 아닌 값을 설정하면 바로 밑의 for문을 실행한다.
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
window.geometry("800x500")
window.resizable(width =False, height = True)

# C:/images 까지 하면 이후에는 이미지가 불러와짐.
folder = askdirectory(parent=window)
##이미지를 불러올 폴더를 선택하라. -> 설명이 필요하면, Code05-05 파일목록 참고.
for dirName, subDirList, fnames in os.walk(folder):
    for fname in fnames:
        if os.path.splitext(fname)[1].upper() == ".GIF":
            fullName = dirName + "/" + fname
            ## '/' 를 기준으로 합쳐야 함.
            fnameList.append(fullName)

# main에서 처음 이미지 보여주기
photo = PhotoImage(file = fnameList[num])
pLabel = Label(window, image = photo)
##이미지만 띄운 것임. 버튼 출력이 아님.

#버튼 출력 부분
btnPrev = Button(window, text = '<< 이전', command = clickPrev)
label1 = Label(window, text=fnameList[num])
btnNext = Button(window, text = '다음>>', command = clickNext)
##Button은 command까지 가능, Label은 command는 불가능.


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
## mainMenu가 클래스이고,(바로 아래)

#이동
fileMenu = Menu(mainMenu)
## fileMenu가 객체라고 생각.(바로 위)

mainMenu.add_cascade(label = "이동", menu = fileMenu)
## mainMenu에 '이동'이라는 라벨을 만들고 그 안에 fileMenu로 처리 하겠다.
fileMenu.add_command(label = "앞으로", command=clickPrev)
## fileMenu에는 '앞으로'라는 라벨이 있고, clickPrev 명령을 실행한다.
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
##위 세개는 default인 count==0을 무시하고, 정수를 넣기 때문에 hopImage에서 count는 각각 1,3,5가 된다.
hopMenu.add_command(label = "원하는 수 ", command = lambda : hopImage())
## hopImage에서 default가 count == 0 이므로 hopImage()로 설정하는 것이 맞다.
hopMenu.add_separator()
hopMenu.add_command(label = "Select File", command = selectFile)

btnPrev.place(x=130, y=10); label1.place(x=200, y=10); btnNext.place(x=500, y=10)
pLabel.place(x=15, y = 50)
window.mainloop()