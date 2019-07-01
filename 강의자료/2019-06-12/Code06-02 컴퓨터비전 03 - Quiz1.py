#[화소점 처리]에 다음 메뉴를 추가하고, 구현하시오.
# (1) 밝게하기
# (2) 어둡게하기
# (3) 영상 곱셈
# (4) 영상 나눗셈
# (5) 화소값 반전 : 0-->255, 1->254 ~~~~
# (6) 이진화(=흑백 영상) : Black/White 2 값으로만 구성된 영상
# (7) 입력/출력 영상의 평균값 구하기 : 출력은 messagebox로
# (8) <선택> Posterizing, Gamma 보정, 명암 대비 스트레칭



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

#밝게하기
def addImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH; outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    value = askinteger("밝게하기", "밝게할 값~~>", minvalue = 1, maxvalue = 255) # 최소 1, 최대 255
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] + value
            if outImage[i][k] >= 255:
                outImage[i][k] = 255
    displayImage()

#어둡게하기

def subImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    value = askinteger("어둡게하기", "어둡게할 값~~>", minvalue=1, maxvalue=255)  # 최소 1, 최대 255
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] - value
            if outImage[i][k] < 0 :
                outImage[i][k] = 0
    displayImage()

#영상 곱셈
def multiImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    value = askinteger("영상 곱하기", "영상 곱하게 할값~~>", minvalue=1, maxvalue=255)  # 최소 1, 최대 255
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = (inImage[i][k] * value)
            if outImage[i][k] > 255:
                outImage[i][k] = 255
    displayImage()

#영상 나눗셈
def divImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    value = askinteger("영상 나누기", "영상 나누게 할 값~~>", minvalue=1, maxvalue=255)  # 최소 1, 최대 255
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = inImage[i][k] // value
            if outImage[i][k] < 0:
                outImage[i][k] = 0
    displayImage()

#화소값 반전
def reverseImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = 255 - inImage[i][k]
    displayImage()

#이진화(=흑백 영상)
def bwImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    # 평균을 기준으로 잡자.
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += inImage[i][k]
    avg = sum // (inW * inH)
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] > avg:
                outImage[i][k] = 255
            else:
                outImage[i][k] = 0
    displayImage()


#입력/출력 영상의 평균값 구하기
def avgImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += inImage[i][k]
    avg = sum / (inH * inW)
    messagebox.showinfo("평균값은 얼마인가요?", avg)
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = int(avg)
    ## 한 사진에 똑같은 숫자들이 입력되면 한 색이 나온다.
    displayImage()

#파라볼라 알고리즘 with LUT
def paraImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########

    #LUT 활용 - 연산 속도가 훨씬 빨라짐.(실무에서 많이 사용)
    LUT = [0 for _ in range(256)]  # LUT가 256개 0으로 초기화
    for input in range(256):
        LUT[input] = int(255 - 255 * math.pow(input / 128 - 1 , 2))
    ## LUT를 먼저 다 만들어준다.

    for i in range(inH):
        for k in range(inW):
            input = inImage[i][k]
            outImage[i][k] = LUT[inImage[i][k]]

    displayImage()

def upDownImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    for i in range(inH):
        for k in range(inW):
            outImage[inH-i-1][k] = inImage[i][k]
    displayImage()
    
#Poster~~~
def posterImage():
    pass

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
window.title("컴퓨터 비전(딥러닝 기법) ver 0.02")

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImage)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImage)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="밝게하기", command=addImage)
comVisionMenu1.add_command(label="어둡게하기", command=subImage)
comVisionMenu1.add_command(label="영상 곱셈", command=multiImage)
comVisionMenu1.add_command(label="영상 나눗셈", command=divImage)
comVisionMenu1.add_command(label="화소값 반전", command=reverseImage)
#comVisionMenu1.add_command(label="흑백 영상", command=bwImage)
comVisionMenu1.add_command(label="입출력 평균값 영상", command=avgImage)
comVisionMenu1.add_command(label="파라볼라", command=paraImage)
#comVisionMenu1.add_command(label="Posterizing", command=posterImage)
#comVisionMenu1.add_command(label="Gamma 보정", command=gammaImage)
#comVisionMenu1.add_command(label="명암 대비 스트레칭", command=)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소(통계)", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화", command=bwImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전", command=upDownImage)


window.mainloop()
