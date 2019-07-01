from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

def func_open():
    global photo, filename
    filename = askopenfilename(parent=window,
     filetypes=(("텍스트 파일", "*.txt;*.ini;*.py"), ("모든 파일", "*.*")))

    with open(filename, 'r') as rFp :
        strList = rFp.readlines()
        memoStr = ''.join(strList)
        txtPanel.insert(END, memoStr)

def func_save():
    memoStr = txtPanel.get("1.0",END)
    with open(filename, 'w') as wFp :
        wFp.writelines(memoStr)
    print('Save. OK~')


def func_change() :
    oldStr = askstring('기존 문자', '기존 문자열-->')
    newStr = askstring('새 문자', '새 문자열-->')
    memoStr = txtPanel.get("1.0", END)
    memoStr = memoStr.replace(oldStr,newStr)
    print(memoStr)
    txtPanel.delete("1.0", END) #1행0열 ~ 끝
    txtPanel.insert(END, memoStr)

def func_copy() :
    global selectStr
    selectStr = txtPanel.selection_get()

def func_paste() :
    global selectStr
    curPos = txtPanel.index(INSERT)
    txtPanel.insert(curPos, selectStr)

# 메인 코드  부분
window = Tk()
#window.geometry("400x400")
window.title("매모장 Ver 0.01")

txtPanel = Text(window, height=20, width=50, bg='yellow')
txtPanel.pack(expand=1, anchor=CENTER)

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=func_open)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=func_save)

editMenu = Menu(mainMenu)
mainMenu.add_cascade(label="편집", menu=editMenu)
editMenu.add_command(label="바꾸기", command=func_change)
editMenu.add_separator()
editMenu.add_command(label="복사", command=func_copy)
editMenu.add_command(label="붙여넣기", command=func_paste)

window.mainloop()

from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import *

def func_open():
    global photo, filename
    filename = askopenfilename(parent=window,
     filetypes=(("텍스트 파일", "*.txt;*.ini;*.py"), ("모든 파일", "*.*")))

    with open(filename, 'r') as rFp :
        strList = rFp.readlines()
        memoStr = ''.join(strList)
        txtPanel.insert(END, memoStr)

def func_save():
    memoStr = txtPanel.get("1.0",END)
    with open(filename, 'w') as wFp :
        wFp.writelines(memoStr)
    print('Save. OK~')


def func_change() :
    oldStr = askstring('기존 문자', '기존 문자열-->')
    newStr = askstring('새 문자', '새 문자열-->')
    memoStr = txtPanel.get("1.0", END)
    memoStr = memoStr.replace(oldStr,newStr)
    print(memoStr)
    txtPanel.delete("1.0", END) #1행0열 ~ 끝
    txtPanel.insert(END, memoStr)

def func_copy() :
    global selectStr
    selectStr = txtPanel.selection_get()

def func_paste() :
    global selectStr
    curPos = txtPanel.index(INSERT)
    txtPanel.insert(curPos, selectStr)

# 메인 코드  부분
window = Tk()
#window.geometry("400x400")
window.title("매모장 Ver 0.01")

txtPanel = Text(window, height=20, width=50, bg='yellow')
txtPanel.pack(expand=1, anchor=CENTER)

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=func_open)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=func_save)

editMenu = Menu(mainMenu)
mainMenu.add_cascade(label="편집", menu=editMenu)
editMenu.add_command(label="바꾸기", command=func_change)
editMenu.add_separator()
editMenu.add_command(label="복사", command=func_copy)
editMenu.add_command(label="붙여넣기", command=func_paste)

window.mainloop()