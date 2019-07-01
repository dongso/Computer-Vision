from tkinter import *
from tkinter import messagebox
def fileClick():
    messagebox.showinfo("Menu", "Content")


window = Tk() # root = Tk()
mainMenu = Menu(window)
## mainMenu에 필요한 것들을 삽입할 것임.
window.config(menu = mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label = '파일', menu=fileMenu)
fileMenu.add_command(label = "열기", command=fileClick)
fileMenu.add_separator()
fileMenu.add_command(label = "종료", command=None)

window.mainloop()


