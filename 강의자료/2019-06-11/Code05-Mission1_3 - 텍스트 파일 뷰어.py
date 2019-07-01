#(3) 텍스트 파일 뷰어를 만들기
#- 메뉴 [파일] >> [열기]에서 텍스트 파일을 선택
#- 선택된 파일을 화면에서 출력(Text 위젯 사용)
#- 파일의 내용을 변경
#- 메뉴 [파일] >> [저장]을 선택하면 파일이 저장됨.
#- (선택) 메뉴에서 [편집] >> [바꾸기] 기능 구현

from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

## 전역변수 선언부
window = None
fileName = None
count = 0

## 함수 선언부

#텍스트 보여주기
def showTxt(x):
    label = Label(window, text = x)
    label.pack()
#파일 열기
def openFile():
    global fileName, count
    fileName = askopenfile()
    fileName = fileName.name
    inFp = open(fileName, "r")
    count = 0
    while True:
        inStr = inFp.readline()
        print(inStr)
        showTxt(inStr) # 함수임.
        if not inStr:
            break
        count += 1
    inFp.close()

#내용 변경
def changeContent():
    global fileName, count
    string = ''
    for i in range(count):
        if i == 0:
            outFp = open(fileName, 'w')
            changeContent = askstring("변경할 문자열을 입력하세요", string)
            showTxt(changeContent)
            outFp.write(changeContent + "\n")
        else:
            outFp = open(fileName, "a")
            changeContent = askstring("변경할 문자열을 입력하세요", string)
            showTxt(changeContent)
            outFp.write(changeContent + "\n")
    ## 처음-> 'w'를 하여 다 지운다, 2번째부터~ 'a'를 활용하여 추가한다.
    outFp.close()

#파일 저장
def saveFile():
    # global fileName
    # saveTxt = open(fileName, "w")
    #saveTxt.write()
    messagebox.showinfo("파일이 저장되었습니다.", "저장 완료!")

    # saveTxt.close()

#파일 바꾸기
def changeFile():
    fileName = askopenfilename(parent = window,
                               filetypes = (("TXT파일", "*.txt;*.raw"), ("모든파일","*.*")))
    print(fileName)
    messagebox.showinfo("파일이 변경되었습니다.", "변경 완료!")

## 메인 코드부
if __name__ == "__main__":
    window = Tk()
    window.title("재정이의 텍스트 파일 뷰어")
    window.geometry("200x200")
    window.resizable(width = False, height = True)

    #메뉴1 - 파일
    mainMenu = Menu(window)
    window.config(menu = mainMenu)

    fileMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "파일", menu = fileMenu)
    fileMenu.add_command(label = "열기", command = openFile)
    fileMenu.add_command(label = "저장", command = saveFile)

    #메뉴2 - 편집
    editMenu = Menu(window)
    window.config(menu = mainMenu)

    editMenu = Menu(mainMenu)
    mainMenu.add_cascade(label = "편집", menu = editMenu)
    editMenu.add_command(label = "바꾸기", command = changeFile)


    #변경 버튼
    btnChange = Button(window, text = "내용 변경", command = changeContent)

    btnChange.pack()
    window.mainloop()



