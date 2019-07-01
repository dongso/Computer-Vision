from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path

###################
### 함수 선언부 ###
###################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h,w):
    retMemory = []
    for _ in range(h):
        tmpList = []
        for _ in range(w):
            tmpList.append(0)
        retMemory.append(tmpList)
    return retMemory
# 파일을 메모리로 로딩하는 함수
def loadImage(fname):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    fsize = os.path.getsize(fname) # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize))  # 핵심 코드 -> 정사각형이므로 루트를 씌우면 가로와 높이가 나옴.

    ## 입력영상 메모리 확보 ## - 512 x 512를 0으로 초기화 시킴.
    inImage = []   # load가 계속 될 수 있기 때문에 초기화 시키는 용도로 사용.
    for _ in range(inH):
        tmpList = []
        for _ in range(inW):
            tmpList.append(0)
        inImage.append(tmpList)
    # 파일 --> 메모리
    with open(filename, 'rb') as rfp:  # 우리는 binary 이므로 rb 사용.(이미지이기 때문에 binary) cf. txt는 r
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rfp.read(1)))   # 1바이트만 읽는다.
    print(inH, inW)
    print(inImage[80][70])
# 파일을 선택해서 메모리로 로딩하는 함수
def openImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    filename = askopenfilename(parent=window,
                filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    loadImage(filename)
    equalImage()

def saveImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    pass

def displayImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    if canvas != None:  # 예전에 실행한 적이 있다.
        canvas.destroy() # canvas를 뽑아냄.
    ## 화면 크기를 조절 -> window -> canvas -> paper를 만듬
    window.geometry(str(outH) + 'x' + str(outW))  # '512 x 512'
    canvas = Canvas(window, height = outH, width = outW)
    paper = PhotoImage(height = outH, width = outW) # 빈 종이 -> PhotoImage로 가져옴.
    canvas.create_image((outH//2, outW//2), image=paper, state='normal') # 종이를 붙이는 데 정중앙 갖다 놓기만 함.(밑에 canvas.pack()에서는 사진을 찍는다)
    ## 출력영상 --> 화면에 한점씩 찍어
    for i in range(outH):   # display는 outH로 찍어야 함
        for k in range(outW):
            r = g = b = outImage[i][k]   # Gray scale이기 때문에 r = g = b로 표현함.
            paper.put("#%02x%02x%02x" % (r, g, b), (k, i)) # 색 표시 할 때 #RRGGBB 에서 각 글자는 0~F까지   %02는 두칸 x
    canvas.pack(expand =1, anchor = CENTER) # 위의 canvas.pack()은 중앙에 점을 찍는다.
#################################################
#### 컴퓨터 비전(영상처리) 알고리즘 함수 모듈 ####
#################################################
## outImage는 알고리즘에 따라 사이즈도 정해질 수 있음.

# 동일영상 알고리즘
def equalImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH; outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k]
    displayImage()

######################
### 전역변수 선언부 ###
######################
inImage, outImage = [], []
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""  # filename은 계속 가지고 다닐 것임.

###################
### 메인 코드부 ###
###################
# 메인 코드  부분
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝 기법) ver 0.01")

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImage)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImage)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="알고리즘A", menu=comVisionMenu1)
comVisionMenu1.add_command(label="알고리즘1", command=None)
comVisionMenu1.add_command(label="알고리즘2", command=None)

window.mainloop()
