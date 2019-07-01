from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
from tkinter import ttk, Canvas
import os # 디스크 접근
import os.path
import math
import numpy
import pymysql
import csv
import xlrd  # 엑셀 읽기
import xlwt
import xlsxwriter

window = Tk()
#window.geometry("500x500")
window.resizable(height = True, width = False) # 창 조절 가능 여부
canvas: Canvas = Canvas(window, width = 500, height = 500)
##window.geometry("500x500")를 안주게 되면 윈도우 창이 캔버스 크기에 의해 변경됨.
paper = PhotoImage(width = 500, height = 500)
canvas.create_image((500 // 2, 500 // 2), image = paper , state = 'normal')
## 이미지를 중앙에 둘 것임.

canvas.pack(expand = 1, anchor = CENTER)
window.mainloop()