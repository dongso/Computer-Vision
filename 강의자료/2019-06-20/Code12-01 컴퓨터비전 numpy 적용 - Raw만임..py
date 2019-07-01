from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import pymysql
import numpy as np

###################
### 함수 선언부 ###
###################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w, initValue = 0, dataType = np.uint8):  # 값을 안받으면 default 0으로 처리.
    retMemory = np.zeros((h,w), dtype=dataType)
    retMemory += initValue
    return retMemory

# 파일을 메모리로 로딩하는 함수
def loadImage(fname):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    fsize = os.path.getsize(fname)  # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize))  # 핵심 코드 -> 정사각형이므로 루트를 씌우면 가로와 높이가 나옴.
    ## 입력영상 메모리 확보 ## - 512 x 512를 0으로 초기화 시킴.
    inImage = np.fromfile(fname, dtype=np.uint8)   #  np.fromfile이 효율적인 binary reading 방법임.
    inImage = inImage.reshape(inH, inW) # inImage를 inH, inW의 배열 형태로 바꿔준다.

# 파일을 선택해서 메모리로 로딩하는 함수
import time
def openImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    start = time.time()
    loadImage(filename)
    equalImage()
    print(time.time() - start)  # 사진 오픈 되는 시간 확인하기 위함.

import struct
def saveImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    saveFp = asksaveasfile(parent = window, mode = 'wb',
            defaultextension="*.raw", filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    for i in range(outH):
        for k in range(outW):
            saveFp.write(struct.pack('B', outImage[i][k]))
    saveFp.close()

def displayImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global VIEW_X, VIEW_Y
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    ## 고정된 화면 크기
    if outH <= VIEW_Y or outW <= VIEW_X :
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else :
        VIEW_X = 512
        VIEW_Y = 512
        step = outW / VIEW_X    # 밑에 numpy.arange(0,outH, step) : 에서 사용하기 위함.

    window.geometry(str(int(VIEW_Y*1.2)) + 'x' + str(int(VIEW_X*1.2)))  # 벽 -> 사진이 512*512이면 좀 더 크게 함으로써 크기를 맞춰주기 위함.
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_Y // 2, VIEW_X // 2), image=paper, state='normal')


    ## 화면 크기를 조절
    # window.geometry(str(outH) + 'x' + str(outW)) # 벽
    # canvas = Canvas(window, height=outH, width=outW) # 보드
    # paper = PhotoImage(height=outH, width=outW) # 빈 종이
    # canvas.create_image((outH//2, outW//2), image=paper, state='normal')
    # ## 출력영상 --> 화면에 한점씩 찍자.
    # for i in range(outH) :
    #     for k in range(outW) :
    #         r = g = b = outImage[i][k]
    #         paper.put("#%02x%02x%02x" % (r, g, b), (k, i))
    ## 성능 개선
    import numpy
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0,outH, step) :   # 예를들어 outH가 1024x1024이면 2칸씩 띄면서 틀 512x512에 이미지를 맞춰준다.
        tmpStr = ''
        for k in numpy.arange(0,outW, step) :
            i = int(i); k = int(k)
            r = g = b = int(outImage[i][k])
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)   # 실질적으로 사진이 화면에 나타나는 코드 부분.

    canvas.bind('<Button-1>', mouseClick)
    canvas.bind('<ButtonRelease-1>', mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

def selectFolder():
    folder = askdirectory(parent = window)
    ##이미지를 불러올 폴더를 선택하라.
    for dirName, subDirList, fnames in os.walk(folder):
        for fname in fnames:
            if os.path.splitext(fname)[1].upper() == ".RAW":
                fullName = dirName + "/" + fname
                ## '/'를 기준으로 합쳐야 함.
                fnameList.append(fullName)
        print(fnameList)

def selectFile() :
    filename = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    edt1.insert(0, str(filename))

import datetime
def uploadData() :
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()

    fullname = edt1.get()

    for i in range(fnameList):
        with open(fullname, 'rb') as rfp :
            binData = rfp.read()
        fname = os.path.basename(fullname)
        fsize = os.path.getsize(fullname)
        height = width = int(math.sqrt(fsize))
        now = datetime.datetime.now()
        upDate = now.strftime('%Y-%m-%d')
        upUser = USER_NAME
        sql = "INSERT INTO rawImage_TBL(raw_id , raw_height , raw_width"
        sql += ", raw_fname , raw_update , raw_uploader, raw_avg , raw_data) "
        sql += " VALUES(NULL," + str(height) + "," + str(width) + ",'"
        sql += fname + "','" + upDate +"','" + upUser + "',0 , "
        sql += " %s )"
        tupleData = (binData,)
        cur.execute(sql, tupleData)
        con.commit()
        cur.close()
        con.close()
        print(sql)

import tempfile
def downloadData() :
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    sql = "SELECT raw_fname, raw_data FROM rawImage_TBL WHERE raw_id = 1"
    cur.execute(sql)
    fname, binData = cur.fetchone()

    fullPath = tempfile.gettempdir() + '/' + fname
    with open(fullPath, 'wb') as wfp :
        wfp.write(binData)
    print(fullPath)
    cur.close()
    con.close()
    print(sql)

#################################################
#### 컴퓨터 비전(영상처리) 알고리즘 함수 모듈 ####
#################################################
## outImage는 알고리즘에 따라 사이즈도 정해질 수 있음.

# 동일영상 알고리즘
def equalImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = inImage.copy() # numpy 자체가 배열이기 때문에 []초기화를 시킬 필요가 없음.
    displayImage()

# 밝게, 어둡게 하기
def addImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ########진짜 컴퓨터 비전 알고리즘 ########
    value = askinteger("밝게/어둡게", "값~~>", minvalue=-255, maxvalue=255)  # 최소 1, 최대 255
    start = time.time()
    inImage = inImage.astype(np.int16)  # 넘파이에서 astype은 형을 바꿔줌. int16은 부호가 있는 16비트 정수형과 부호가 없는 16비트 정수형
    outImage = inImage + value

    seconds = time.time() - start
    displayImage()
    status.configure(text = status.cget("text") + "\t\t 시간(초):"
                     + "{0:.2f}".format(seconds)) # addImage()를 하게 되면, 오른쪽 하단에 몇 초만에 로딩이 되었는지 알려줌.

# 영상 곱셈
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


# 영상 나눗셈
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

# 화소값 반전
def reverseImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###############메모리할당####################
    ########진짜 컴퓨터 비전 알고리즘 ########
    outImage = 255 - inImage
    displayImage()

# 이진화(=흑백 영상)
def bwImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ##############메모리 할당############
    ########진짜 컴퓨터 비전 알고리즘 ########
    ## 영상의 평균 구하기 ##
    outImage = malloc(outH, outW)
    avg = np.average(inImage)
    outImage = np.where(outImage > avg, 255, 0) # np.where가 R의 ifelse와 비슷.
    displayImage()

# 파라볼라 알고리즘 with LUT
def paraImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    x = np.array([i for i in range(0,256)])
    LUT = 255 - 255*np.power(x / 128 -1, 2)    #  np.power(a,b)는 a^b  => 따라서 x 값을 대입하여, 파라볼라 형태 LUT를 만들어준다.
    LUT = LUT.astype(np.uint8)  # uint8은 부호가 있는 8비트(1바이트) 정수형과 부호가 없는 8비트 정수형 / np.uint8은 넘파이에서 메모리 확보를 위한 자료형. C언어에서 long 하는 것처럼.

    displayImage()

# 상하반전 알고리즘
def upDownImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ##############메모리 할당#############
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    # outImage = inImage[::-1, ::1]  # np에서 거꾸로 읽어줌. 상하이기 때문에 열은 그대로, 행만 거꾸로 뒤집음.
    outImage = np.flip(inImage, axis = 0) # axis = 1을 하면 행을 의미하는데, 좌우가 바뀐다.
    ## 상하가 바뀌었다는 것은 같은 열에서 맨 위의 값과 맨 밑의 값이 바뀌어야 한다. 따라서,
    ##열은 변화가 없고, 행 값만 역으로 해주면 된다. inH - i - 1 값을 취하면 상하가 바뀌게 된다.
    displayImage()

# 화면이동 알고리즘
def moveImage():
    global panYN
    panYN = True  # 마우스가 먹음
    canvas.configure(cursor = 'mouse')

def mouseClick(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey, panYN
    if panYN == False:   # 진행하지 말아라. 마우스 클릭 해봤자 아무 반응도 안함.
        return
    sx = event.x; sy = event.y   # 클릭해라.

def mouseDrop(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey, panYN
    if panYN == False:   # 진행하지 말아라. 마우스 클릭 해봤자 아무 반응도 안함.
        return
    ex = event.x; ey = event.y
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    mx = sx - ex; my = sy - ey   # x, y에 대한 이동 양
    for i in range(inH):
        for k in range(inW):
            if 0 <= i-my < outW and 0 <= k-mx < outH:
                outImage[i-my][k-mx] = inImage[i][k]
    panYN = False
    displayImage()

#영상 축소 알고리즘
def zoomOutImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    value = askinteger("축소", "값~~>", minvalue=2, maxvalue=16)  # 최소 1, 최대 255
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH//value
    outW = inW//value
    ###############메모리 할당###############
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    # backwarding 기법
    outImage = inImage.copy()
    outImage = inImage[::value, ::value]  # outImage
    displayImage()

    # forwarding 기법
    #위 보다 성능이 덜 좋다. 위는 outH로 돌리기 때문에 훨씬 빨리 돈다.
    # for i in range(inH):
    #     for k in range(inW):
    #         outImage[i//value][k//value] = inImage[i][k]
    # displayImage()

#영상 축소 알고리즘(평균변환)
def zoomOutImage2():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    value = askinteger("축소", "값~~>", minvalue=2, maxvalue=16)  # 최소 1, 최대 255
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH//value
    outW = inW//value
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    for i in range(inH):
        for k in range(inW):
            outImage[i//value][k//value] += inImage[i][k]
    for i in range(outH):
        for k in range(outW):
            outImage[i][k] //= (value*value)

    displayImage()

#영상 확대 알고리즘
def zoomInImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    value = askinteger("확대", "값~~>", minvalue=2, maxvalue=8)  # 최소 1, 최대 255
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH * value
    outW = inW * value
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    outImage = np.kron(inImage, np.ones((value, value)))  # np.ones((2,2))은 1이 2x2 크기 만큼 차있음.
    # >> > np.kron([1, 10, 100], [5, 6, 7])
    # array([5, 6, 7, 50, 60, 70, 500, 600, 700])
    print(outImage)
    displayImage()

    # forwarding 기법
    # for i in range(inH):
    #     for k in range(inW):
    #         outImage[i*value][k*value] = inImage[i][k]
    # displayImage()

# 영상 확대 알고리즘 (양선형 보간) -> 영상 품질을 향상시킬 수 있음.
def zoomInImage2():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    value = askinteger("확대", "값~~>", minvalue=2, maxvalue=4)  # 최소 1, 최대 255
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH * value
    outW = inW * value
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    rH, rW, iH, iW = [0] * 4 # 실수위치 및 정수 위치   / real integer
    x,y = 0, 0 # 실수와 정수의 차이값
    C1,C2,C3,C4 = [0] * 4 # 결정할 위치(N)의 상하좌우 픽셀
    for i in range(outH):
        for k in range(outW):
            rH = i / value; rW = k / value    # 확대하기 때문에 나눠야 함.
            iH = int(rH); iW = int(rW)   # 나눈 값을 정수로 나타냄.
            x = rW - iW; y = rH - iH  #
            if 0 <= iH < inH-1 and 0 <= iW < inW-1:
                C1 = inImage[iH][iW]
                C2 = inImage[iH][iW + 1]
                C3 = inImage[iH+1][iW+1]
                C4 = inImage[iH+1][iW]
                newValue = C1*(1-y)*(1-x) + C2*(1-y)*x + C3*y*x + C4*y*(1-x)
                outImage[i][k] = int(newValue)
    displayImage()

# 영상 회전 알고리즘
def rotateImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    angle = askinteger("회전", "값~~>", minvalue=1, maxvalue=360)
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    radian = angle * math.pi / 180
    for i in range(inH):
        for k in range(inW):
            xs = i; ys = k;
            xd = int(math.cos(radian) * xs - math.sin(radian) *ys)
            yd = int(math.sin(radian) * xs + math.sin(radian) *ys)
            if 0 <= xd < inH and 0 <= yd < inW :
                outImage[xd][yd] = inImage[i][k]
    displayImage()

# 영상 회전 알고리즘 - 중심, 역방향
def  rotateImage2() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    cx = inW//2; cy = inH//2   # (cx, cy)는 중심점.
    for i in range(outH) :
        for k in range(outW) :
            xs = i ; ys = k;
            xd = int(math.cos(radian) * (xs-cx) - math.sin(radian) * (ys-cy)) + cx
            yd = int(math.sin(radian) * (xs-cx) + math.cos(radian) * (ys-cy)) + cy
            if 0<= xd < outH and 0 <= yd < outW :
                outImage[xs][ys] = inImage[xd][yd]
            else :
                outImage[xs][ys] = 255

    displayImage()


# 히스토그램 -> 영상 그래프를 시각적으로 확인하기 위함.
import matplotlib.pyplot as plt
def histoImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    inCountList = [0] * 256
    outCountList = [0] * 256

    for i in range(inH):
        for k in range(inW):
            inCountList[inImage[i][k]] += 1

    for i in range(outH):
        for k in range(outW):
            outCountList[outImage[i][k]] += 1

    plt.plot(outCountList)
    plt.plot(inCountList)
    plt.show()

#히스토그램 -> matplotlib 사용 없이 진행.
def histoImage2():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    outCountList = [0] * 256
    normalCountList = [0] * 256

    #빈도수 계산
    for i in range(outH):
        for k in range(outW):
            outCountList[outImage[i][k]] += 1
    maxVal = max(outCountList); minVal = min(outCountList)
    High = 256
    # 정규화 = (카운트 값 - 최소값) * High / (최대값 - 최소값)
    for i in range(len(outCountList)):
        normalCountList[i] = (outCountList[i] - minVal) * High / (maxVal - minVal)

    ## 서브 윈도창 생성 후 출력
    subWindow = Toplevel(window)
    subWindow.geometry('256x256')
    subCanvas = Canvas(subWindow, width=256,height = 256)
    subPaper = PhotoImage(width = 256, height = 256)
    subCanvas.create_image((256//2, 256//2), image = subPaper, state='normal')
    print(max(normalCountList))
    for i in range(len(normalCountList)):   # 255번 돌아감.
        for k in range(int(normalCountList[i])): # 0 <= normalCountList[i] <= 256
            data = 0   # data=0으로 해준 이유는 검은색만 나오게 하기 위함.
            subPaper.put('#%02x%02x%02x' % (data,data,data), (i,255-k)) #subPaper.put(색, 좌표) / (i, 255-k)에서 i는 x축이고, 255-k인 이유는 밑에서 부터 시작하기 위함.
            ## for k in range()를 해서 y축 방향으로 색을 계속 칠한다.
    subCanvas.pack(expand=1, anchor = CENTER)
    subWindow.mainloop()
# 스트레칭 알고리즘(명암)
def stretchImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    maxVal = minVal = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]

    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = int(((inImage[i][k] - minVal) / (maxVal - minVal)) * 255)
    displayImage()

def endinImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    maxVal = minVal = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]

    minAdd = askinteger("최소", "최소추가~~>", minvalue=0, maxvalue=255)
    maxAdd = askinteger("최대", "최소감소~~>", minvalue=0, maxvalue=255)

    minVal += minAdd
    maxVal -= maxAdd

    for i in range(inH):
        for k in range(inW):
            value = int((inImage[i][k] - minVal) / (maxVal - minVal)) * 255
            if value <0:
                value = 0
            elif value >255:
                value = 255
            outImage[i][k] = value
    displayImage()

# 평활화 - 강사님 방법
def smoothImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    histo = [0] * 256; sumHisto = [0] * 256; normalHisto =[0] * 256
    # 1. 빈도 수 조사
    for i in range(inH):
        for k in range(inW):
            histo[inImage[i][k]] += 1
    # 2. 누적 히스토그램 생성
    sValue = 0
    for i in range(len(histo)):
        sValue += histo[i]  # 누적 값. 계속 합쳐짐.
        sumHisto[i] = sValue
    # 3. 정규화 누적 히스토그램
    for i in range(len(sumHisto)):
        normalHisto[i] = int(sumHisto[i] / (inW * inH) * 255)
        ## inW * inH는 총 픽셀 수
    # 4. 영상처리
    for i in range(inH):
        for k in range(inW):
            outImage[i][k] = normalHisto[inImage[i][k]]
    displayImage()

# 엠보싱 처리
def embossImage():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    outImage = malloc(outH, outW)
    ########진짜 컴퓨터 비전 알고리즘 ########
    MSIZE = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]

    ## 임시 입력영상 메모리 확보 -> Input 메모리 확보를 위한.
    tmpInImage = malloc(inH + (MSIZE - 1), inW + (MSIZE -1), 127)  # 127은 중간값 / 마스크에 따라 바깥 처리를 달리한다.
    tmpOutImage = malloc(outH, outW)
    ## 원 입력 ~~> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImage[i+MSIZE//2][k+MSIZE//2] = inImage[i][k]   # 바깥 쪽 값 입력

    ## 회선연산
    for i in range(MSIZE//2, inH + MSIZE//2):   # 큰 틀이 주가 아니라, 더 안쪽의 값이 inputImage임
        for k in range(MSIZE//2, inW + MSIZE//2):
            # 각 점을 처리
            S = 0.0# S는 누적값
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImage[i + m - MSIZE//2][k + n - MSIZE//2]
            tmpOutImage[i-MSIZE//2][k-MSIZE//2] = S
    ## 127 더하기 -> 선택해서 진행.
    for i in range(outH):
        for k in range(outW):
            tmpOutImage[i][k] += 127
    ## 임시 출력 --> 원 출력
    for i in range(outH):
        for k in range(outW):
            value = tmpOutImage[i][k]
            if value > 255:
                value = 255
            elif value < 0:
                value = 0
            outImage[i][k] = int(value)
    displayImage()

# 모핑 알고리즘
def morphImage() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                               filetypes=(("RAW 파일", "*.raw"), ("모든 파일", "*.*")))
    if filename2 == '' or filename2 == None:
        return

    fsize = os.path.getsize(filename2)  # 파일의 크기(바이트)
    inH2 = inW2 = int(math.sqrt(fsize))  # 핵심 코드
    ## 입력영상 메모리 확보 ##
    inImage2 = []
    inImage2 = malloc(inH2, inW2)
    # 파일 --> 메모리
    with open(filename2, 'rb') as rFp:
        for i in range(inH2):
            for k in range(inW2):
                inImage2[i][k] = int(ord(rFp.read(1))) # ord는 아스키코드 리턴
    ###### 메모리 할당 ################
    outImage = [];    outImage = malloc(outH, outW)
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    #w1 = askinteger("원영상 가중치", "가중치(%)->", minvalue=0, maxvalue=100)
    #w2 = 1- (w1/100);    w1 = 1-w2

    import threading
    import time
    def morpFunc() :
        w1 = 1;        w2 = 0
        for _ in range(20) :  # 20은 0.05 * 20 = 1을 만들어주기 위함.
            for i in range(inH) :
                for k in range(inW) :
                    newValue = int(inImage[i][k]*w1 + inImage2[i][k]*w2)  # 초기에는 inImage[i][k]가 있다가 점점 어두워지고, inImage2[i][k]가 밝아짐.
                    if newValue > 255 :
                        newValue = 255
                    elif newValue < 0 :
                        newValue = 0
                    outImage[i][k] =newValue
            displayImage()
            w1 -= 0.05;        w2 += 0.05
            time.sleep(0.5)

    threading.Thread(target=morpFunc).start()

## 임시 경로에 outImage를 저장하기.
#-> 이미지를 바로 DB에 넣을 수 없기 때문에 파일로 변환하여 DB에 넣는 과정
import random
def saveTempImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    import tempfile
    saveFp = tempfile.gettempdir() + "/" + str(random.randint(10000,99999)) + ".raw"
    ## .raw 파일이 겹치지 않도록.
    if saveFp == '' or saveFp == None:
        return
    print(saveFp)
    saveFp = open(saveFp, mode = 'wb')
    for i in range(outH):
        for k in range(outW):
            saveFp.write(struct.pack('B', outImage[i][k]))
    saveFp.close()
    return saveFp

def findStat(fname):
    # 파일 열고, 읽기.
    fsize = os.path.getsize(fname)  # 파일의 크기(바이트)
    inH = inW = int(math.sqrt(fsize)) # 핵심 코드
    ##입력 영상 메모리 확보##
    inImage= []
    inImage= malloc(inH, inW)
    #파일 --> 메모리
    with open(fname, 'rb') as rFp:
        for i in range(inH):
            for k in range(inW):
                inImage[i][k] = int(ord(rFp.read(1)))
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += inImage[i][k]
    avg = sum // (inW * inH)
    maxVal = minVal = inImage[0][0]
    for i in range(inH):
        for k in range(inW):
            if inImage[i][k] < minVal:
                minVal = inImage[i][k]
            elif inImage[i][k] > maxVal:
                maxVal = inImage[i][k]
    return avg, maxVal, minVal

import pymysql
IP_ADDR = '192.168.56.106'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET = 'utf8'
def saveMysql():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user =USER_NAME, password=USER_PASS,
                          db = DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    try:
        sql = '''
                CREATE TABLE rawImage_TBL (
                raw_id INT AUTO_INCREMENT PRIMARY KEY,
                raw_fname VARCHAR(30),
                raw_extname CHAR(5),
                raw_height SMALLINT, raw_width SMALLINT,
                raw_avg TINYINT UNSIGNED,
                raw_max TINYINT UNSIGNED, raw_min TINYINT UNSIGNED,
                raw_data LONGBLOB);
        '''
        ## SMALLINT 는 2바이트 / TINYINT는 1바이트 LONGBLOB은 DB에 파일을 저장해놓는 형식
        cur.execute(sql)
    except:
        pass

    ## outImage를 임시 폴더에 저장하고, 이걸 fullname으로 전달.
    fullname = saveTempImage()
    fullname = fullname.name
    with open(fullname, 'rb') as rfp:
        binData = rfp.read()

    fname, extname = os.path.basename(fullname).split(".")
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))
    avgVal, maxVal, minValue = findStat(fullname)  # 평균,최대,최소
    sql = "INSERT INTO rawImage_TBL(raw_id, raw_fname, raw_extname,"
    sql += "raw_height, raw_width, raw_avg, raw_max, raw_min, raw_data) "
    sql += " VALUES(NULL,'" + fname + "','" + extname + "',"
    sql += str(height) + "," + str(width) + ","
    sql += str(avgVal) + "," + str(maxVal) + "," + str(minValue)
    sql += ", %s )"
    tupleData = (binData,)
    cur.execute(sql, tupleData)
    con.commit()
    cur.close()
    con.close()
    os.remove(fullname)
    print("업로드 OK -->" + fullname)


def loadMysql():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    sql = "SELECT raw_id, raw_fname, raw_extname, raw_height, raw_width "
    sql += "FROM rawImage_TBL"
    cur.execute(sql)

    queryList = cur.fetchall()  # 전체 불러오기.
    print(queryList)
    rowList = [':'.join(map(str,row)) for row in queryList]
    import tempfile  # C:\Users\user\AppData\Local\Temp 로 가도록 하는 라이브러리가 tempfile -> 요기에서 조작.
    def selectRecord():
        global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
        selIndex = listbox.curselection()[0]  # 0, 1, 2 ... 순으로 나온다.
        subWindow.destroy()  # 선택을 하면 subWindow 창을 닫는다.
        raw_id = queryList[selIndex][0]
        sql = "SELECT raw_fname, raw_extname, raw_data FROM rawImage_TBL "
        sql += "WHERE raw_id = " + str(raw_id)    
        cur.execute(sql)   # 이 줄부터 위 두 줄은 이미지에서 필요한 것들만 가져옴.
        fname, extname, binData = cur.fetchone()
        print()
        fullPath = tempfile.gettempdir() + '/' + fname + "." + extname # C:\Users\user\AppData\Local\Temp/64319.raw 형태로 저장.
        with open(fullPath, 'wb') as wfp:  # 이 과정을 진행하지 않으면 펜은 있는데 종이는 없는 느낌. with문 과정이 반드시 필요. 후에 뒤에서 삭제를 해줘야 함.
            wfp.write(binData)            #
        cur.close()
        con.close()
        print(tempfile)

        loadImage(fullPath)   # 메모리에 적재만 되었고 equalImage에서 display가 된다.
        equalImage()
        os.remove(fullPath)  # os.remove 를 진행하지 않으면 Appdata 로컬 안에 있는 임시 파일이 계속 쌓이게 되어, 반드시 제거를 해줘야 한다.


    ## 서브 윈도에 목록 출력하기
    subWindow = Toplevel(window)
    listbox = Listbox(subWindow)
    button = Button(subWindow, text="선택", command = selectRecord)

    for rowStr in rowList:
        listbox.insert(END, rowStr)

    listbox.pack(expand = 1, anchor = CENTER)
    button.pack()
    subWindow.mainloop()

    cur.close()
    con.close()

# 파일을 메로리로 로딩하는 함수
def loadCSV(fname):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    fsize = 0
    fp = open(fname, 'r')
    for _ in fp:
        fsize += 1
    inH = inW = int(math.sqrt(fsize))  # 핵심 코드
    fp.close()
    ## 입력영상 메모리 확보 ##
    inImage = []
    inImage = malloc(inH, inW)
    # 파일 --> 메모리
    with open(fname, 'r') as rFp:
        for row_list in rFp:
            row, col, value = list(map(int, row_list.strip().split(",")))
            inImage[row][col] = value

def openCSV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent = window,
            filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    loadCSV(filename)
    equalImage()

import csv
def saveCSV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent = window, mode = 'wb',
                           defaultextension = '*.csv', filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return
    with open(saveFp.name, 'w', newline='') as wFp:
        csvWriter = csv.writer(wFp)
        for i in range(outH):
            for k in range(outW):
                row_list = [i, k, outImage[i][k]]
                csvWriter.writerow(row_list)
    print("CSV.save OK~")

import xlwt
def saveExcel():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='*.xls', filetypes=(("XLS 파일", "*.xls"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    xlsName = saveFp.name
    sheetName = os.path.basename(filename)
    wb = xlwt.Workbook()
    ws = wb.add_sheet(sheetName)

    for i in range(outH):
        for k in range(outW):
            ws.write(i, k, outImage[i][k])

    wb.save(xlsName)
    print("Excel.save OK~~")

import xlsxwriter
def saveExcelArt():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='*.xls', filetypes=(("XLS 파일", "*.xls"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return
    xlsName = saveFp.name
    sheetName = os.path.basename(filename)

    wb = xlsxwriter.Workbook(xlsName)
    ws = wb.add_worksheet(sheetName)

    ws.set_column(0, outW-1, 1.0)#약 0.34
    for i in range(outH):
        ws.set_row(i, 9.5) # 약 0.35

    for i in range(outH):
        for k in range(outW):
            data = outImage[i][k]
            # data 값으로 셀의 배경색을 조절 #000000 ~ #FFFFFF
            if data > 15:
                hexStr = '#' + hex(data)[2:]*3
            else:
                hexStr = '#' + ('0' + hex(data)[2:]) * 3
#            print(hex)    # <built-in function hex>
#            print(hex(data))  # 0x5b
#            print(hex(data)[2:])  # 5b
#            print(hex(data)[2:]*3)  # 5b5b5b
            # 셀의 포맷을 준비
            cell_format = wb.add_format()
            cell_format.set_bg_color(hexStr)
            ws.write(i, k, '', cell_format)
#    print(cell_format)   # <xlsxwriter.format.Format object at 0x000001F131F9C9E8>
#    print(cell_format.set_bg_color)  # <bound method Format.set_bg_color of <xlsxwriter.format.Format object at 0x000001F131F9C9E8>>
#    print(cell_format.set_bg_color(hexStr))
    wb.close()
    print("Excel Art.save OK~~~~")

def openExcel():
    pass

######################
### 전역변수 선언부 ###
######################
inImage, outImage = [], []
## inImage는 사진 로드 했을 때의 값
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""  # filename은 계속 가지고 다닐 것임.
panYN = False
sx,sy,ex,ey = [0] * 4
IP_ADDR = '192.168.56.106'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET = 'utf8'
fnameList = []  # 폴더 안에 파일들을 리스트로 두기.
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기(출력용)

###################
### 메인 코드부 ###
###################
# 메인 코드  부분
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝 기법) ver 0.03")

status = Label(window, text='이미지 정보:', bd = 1, relief=SUNKEN, anchor=W) # 창 하단에 '이미지 정보'라고 뜸.
status.pack(side = BOTTOM, fill = X)

## 마우스 이벤트
window.bind("")

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
comVisionMenu1.add_command(label="영상 곱셈", command=multiImage)
comVisionMenu1.add_command(label="영상 나눗셈", command=divImage)
comVisionMenu1.add_command(label="화소값 반전", command=reverseImage)
# comVisionMenu1.add_command(label="흑백 영상", command=bwImage)
comVisionMenu1.add_command(label="파라볼라", command=paraImage)
# comVisionMenu1.add_command(label="Posterizing", command=posterImage)
# comVisionMenu1.add_command(label="Gamma 보정", command=gammaImage)
# comVisionMenu1.add_command(label="명암 대비 스트레칭", command=)
comVisionMenu1.add_command(label="모핑", command=morphImage)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="화소(통계)", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화", command=bwImage)
comVisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImage2)
comVisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImage2)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label = "히스토그램", command=histoImage)
comVisionMenu2.add_command(label = "히스토그램 matplotlib 없이", command=histoImage2)
comVisionMenu2.add_command(label = "명암대비", command=stretchImage)
comVisionMenu2.add_command(label = "End-In탐색", command=endinImage)
comVisionMenu2.add_command(label = "평활화", command=smoothImage)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전", command=upDownImage)
comVisionMenu3.add_command(label="이동", command=moveImage)
comVisionMenu3.add_command(label="확대", command=zoomInImage)
comVisionMenu3.add_command(label="축소", command=zoomOutImage)
comVisionMenu3.add_command(label="회전", command=rotateImage)
comVisionMenu3.add_command(label="회전2(중심,역방향)", command=rotateImage2)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소영역처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱", command=embossImage)

comVisionMenu5 = Menu(mainMenu)
mainMenu.add_cascade(label="기타 입출력", menu =comVisionMenu5)
comVisionMenu5.add_command(label="MYSQL에서 불러오기", command = loadMysql)
comVisionMenu5.add_command(label="MYSQL에서 저장하기", command = saveMysql)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="CSV 열기", command=openCSV)
comVisionMenu5.add_command(label="CSV로 저장하기", command=saveCSV)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="엑셀 열기", command=openExcel)
comVisionMenu5.add_command(label="엑셀로 저장", command=saveExcel)
comVisionMenu5.add_command(label="엑셀 아트로 저장", command=saveExcelArt)

window.mainloop()