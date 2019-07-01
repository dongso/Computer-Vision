# 이벤트(p.304)
#
from tkinter import *
from tkinter import messagebox
def clickLeft(event):
    txt = ''
    if event.num == 1:
        txt += "왼쪽 버튼 : "
    elif event.num == 2:
        txt += "가운데 버튼 : "
    else:
        txt += "오른쪽 버튼 : "
    txt += str(event.x) + "," + str(event.y)
    messagebox.showinfo("요기제목", txt)
    #messagebox.showinfo("요기제목", "요기내용")

def keyPress(event):
    messagebox.showinfo("요기제목", chr(event.keycode))

window = Tk()
window.geometry("500x300")


photo = PhotoImage(file = "C:/images/Pet_GIF/Pet_GIF(256x256)/etc15_256.gif")
label1 = Label(window, image = photo)
window.bind("<Button>", clickLeft)

window.bind("<Key>", keyPress)
## 키보드 다른 값 입력 가능.
#window.bind("a", keyPress)
## 키보드 a만 입력 가능.

label1.pack(expand=1, anchor=CENTER)
window.mainloop()