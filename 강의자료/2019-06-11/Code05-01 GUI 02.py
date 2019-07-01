from tkinter import *
from tkinter import messagebox
def clickButton():
    messagebox.showinfo("요기제목", "요기내용")

window = Tk() #root = Tk()

label1 = Label(window, text="파이썬 공부중~~")
label2 = Label(window, text="파이썬 공부중~~", font=("궁서체", 30), fg="blue")
label3 = Label(window, text="파이썬 ", bg= "red", width=20, height=5, anchor=SE)
##anchor는 위치를 SE(South East)에 두자!!

photo = PhotoImage(file = "C:/images/Pet_GIF/Pet_GIF(256x256)/etc15_256.gif")
## 사진을 준비해서
label4 = Label(window, image = photo)
## 사진에 띄어보자.
button1 = Button(window, text="나를 눌러줘", command = clickButton)
##clickButton은 콜백함수인데, 콜백함수는 clickButton()을 하면 안됨.(python - 2019-06-11 typora 참고)
button2 = Button(window, image=photo, command = clickButton)



label1.pack(); label2.pack();label3.pack();label4.pack(side = LEFT);button1.pack();button2.pack()
## side는 pack에 넣는다.
window.mainloop()
