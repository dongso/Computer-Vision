# 컴퓨터 비전(딥러닝) 칼러비전을 완료하기
# <심화> 추가로 기능을 구현하기

from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
import pymysql
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import time
import cv2
# 파일을 선택해서 메모리로 로딩하는 함수

####################
# 메모리를 할당해서 리스트(참조)를 반환하는 함수
def malloc(h, w, initValue=0) :
    retMemory= []
    for _ in range(h) :
        tmpList = []
        for _ in range(w) :
            tmpList.append(initValue)
        retMemory.append(tmpList)
    return retMemory

# 파일을 메모리로 로딩하는 함수
def loadImageColor(fnameOrCvData) :  # 파일명 or OpenCV 개체
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo,cvPhoto
    inImage = []

    ##################################
    ## PIL 개체 --> OpenCV 개체로 복사.
    if type(fnameOrCvData) == str:
        cvData = cv2.imread(fnameOrCvData)  # 파일 --> cvData개체로 읽어옴.
    else:
        cvData = fnameOrCvData
    cvPhoto = cv2.cvtColor(cvData, cv2.COLOR_BGR2RGB) # 중요! CV개체.
    photo = Image.fromarray(cvPhoto)  # 중요! PIL(pillow) 객체
    inW = photo.width;
    inH = photo.height  # 불러오는 사진의 크기
    ##################################

    ## 메모리 확보
    for _ in range(3) :  # 3면 확보
        inImage.append(malloc(inH, inW))
    photoRGB = photo.convert('RGB')   # RGB색을 만들기 위함.
    print(photoRGB)
    for i in range(inH) :
        for k in range(inW) :
            r, g, b = photoRGB.getpixel((k,i))   # (163, 58, 73) 형태로 나옴. jpg이기 때문에 기존 raw와는 다르다.
            inImage[R][i][k] = r
            inImage[G][i][k] = g
            inImage[B][i][k] = b

def openImageColor() :
    global window, canvas, paper, filename, inImage, outImage,inH, inW, outH, outW
    filename = askopenfilename(parent=window,
                filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename == '' or filename == None :
        return
    loadImageColor(filename)  # load를 하면, 불러온 사진에서 inImage의 픽셀 값이 저장됨.
    equalImageColor()

def displayImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    global VIEW_X, VIEW_Y
    #가로/세로 비율 계산
    ratio = outH / outW
    ## 고정된 화면 크기
    if outH <= VIEW_Y or outW <= VIEW_X:
        VIEW_X = outW
        VIEW_Y = outH
        step = 1
    else:
        VIEW_X = 512
        VIEW_Y = 512
        step = outW / VIEW_X

    window.geometry(str(int(VIEW_X*1.2)) + 'x' + str(int(VIEW_Y*1.2)))  # 벽
    canvas = Canvas(window, height=VIEW_Y, width=VIEW_X)
    paper = PhotoImage(height=VIEW_Y, width=VIEW_X)
    canvas.create_image((VIEW_X // 2, VIEW_Y // 2), image=paper, state='normal')

    import numpy
    rgbStr = '' # 전체 픽셀의 문자열을 저장
    for i in numpy.arange(0,outH, step) :
        tmpStr = ''
        for k in numpy.arange(0,outW, step) :
            i = int(i); k = int(k)
            r , g, b = outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))


import numpy as np
# JGG 파일이 임시 저장소에 저장. (AppData) -> 참고로, RAW와 jpg 저장 방식은 다르다.(내가 여기서 고민 많이 함.)
def saveImageColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if outImage == None :
        return
    outArray = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tup = tuple([outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]])
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), 'RGB')
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='.', filetypes=(("그림 파일", "*.png;*.jpg;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if saveFp == '' or saveFp == None:
        return

    savePhoto.save(saveFp.name)
    print('Save~')

###############################################
##### 컴퓨터 비전(영상처리) 알고리즘 함수 모음 #####
###############################################
# 동일영상 알고리즘
def equalImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    for RGB in range(3) :  # RGB가 0면, 1면, 2면으로 값이 저장됨.
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][i][k] = inImage[RGB][i][k]
    #############################
    displayImageColor()

def addImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ## 메모리 확보
    outImage = []   # 이미지를 불러올 때 outImage에 값이 저장되어 있기 때문에 초기화를 시켜줘야 한다.
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    value = askinteger("밝게/어둡게", "값-->", minvalue=-255, maxvalue=255)
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                if inImage[RGB][i][k] + value > 255 :
                    outImage[RGB][i][k] = 255
                elif inImage[RGB][i][k] + value < 0 :
                    outImage[RGB][i][k] = 0
                else :
                    outImage[RGB][i][k] = inImage[RGB][i][k] + value
    #############################
    displayImageColor()

def revImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = 255 - inImage[RGB][i][k]
    #############################
    displayImageColor()

def paraImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ############################
    ### 진짜 컴퓨터 비전 알고리즘 ###\
    LUT = [0 for _ in range(256)]
    for input in range(256):
        LUT[input] = int(255 - 255 * math.pow(input / 128 - 1, 2))   # 파라볼라 값을 적용한 픽셀.

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = LUT[inImage[RGB][i][k]]
    #############################
    displayImageColor()

def morphImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;
    outW = inW;
    ## 추가 영상 선택
    filename2 = askopenfilename(parent=window,
                               filetypes=(("칼라 파일", "*.jpg;*.png;*.bmp;*.tif"), ("모든 파일", "*.*")))
    if filename2 == '' or filename2 == None:
        return
    inImage2 = []
    photo2 = Image.open(filename2) # PIL 객체
    inW2 = photo2.width; inH2=photo2.height
    ## 메모리 확보
    for _ in range(3) :
        inImage2.append(malloc(inH2, inW2))

    photoRGB2 = photo2.convert('RGB')
    for i in range(inH2) :
        for k in range(inW2) :
            r, g, b = photoRGB2.getpixel((k,i))
            inImage2[R][i][k] = r
            inImage2[G][i][k] = g
            inImage2[B][i][k] = b

    ## 메모리 확보
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))

    import threading
    import time
    def morpFunc():
        w1 = 1;
        w2 = 0
        for _ in range(20):   # 20번 깜빡
            for RGB in range(3) :
                for i in range(inH):
                    for k in range(inW):
                        newValue = int(inImage[RGB][i][k] * w1 + inImage2[RGB][i][k] * w2) # 하나는 꺼지고, 다른 하나는 켜지는 과정.
                        if newValue > 255:
                            newValue = 255
                        elif newValue < 0:
                            newValue = 0
                        outImage[RGB][i][k] = newValue
            displayImageColor()
            w1 -= 0.05   # 점점 픽셀 값이 작아지고,
            w2 += 0.05   # 점점 픽셀 값이 커짐.
            time.sleep(0.5)  # 시간을 0.5초로 잡자.

    threading.Thread(target=morpFunc).start()

# 상하반전 알고리즘
def upDownImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3) :
        for i in range(inH) :
            for k in range(inW) :
                outImage[RGB][inH-i-1][k] = inImage[RGB][i][k]
    displayImageColor()

# 화면이동 알고리즘
def moveImageColor():
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
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    mx = sx - ex; my = sy - ey   # x, y에 대한 이동 양
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if 0 <= i-my < outW and 0 <= k-mx < outH:
                    outImage[RGB][i-my][k-mx] = inImage[RGB][i][k]
    panYN = False
    displayImageColor()

# 영상 축소 알고리즘
def zoomOutImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("축소", "값-->", minvalue=2, maxvalue=16)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH//scale;  outW = inW//scale;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                outImage[RGB][i][k] = inImage[RGB][i*scale][k*scale]

    displayImageColor()

# 영상 확대 알고리즘
def  zoomInImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    scale = askinteger("확대", "값-->", minvalue=2, maxvalue=8)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH*scale;  outW = inW*scale;
    ###### 메모리 할당 ################
    outImage = [];
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    for RGB in range(3) :
        for i in range(outH) :
            for k in range(outW) :
                outImage[RGB][i][k] = inImage[RGB][i//scale][k//scale]
    displayImageColor()

# 영상 회전 알고리즘
def rotateImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    angle = askinteger("회전", "값~~>", minvalue=1, maxvalue=360)
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ############메모리 할당###################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    radian = angle * math.pi / 180
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                xs = i; ys = k;
                xd = int(math.cos(radian) * xs - math.sin(radian) *ys)
                yd = int(math.sin(radian) * xs + math.sin(radian) *ys)
                if 0 <= xd < inH and 0 <= yd < inW :
                    outImage[RGB][xd][yd] = inImage[RGB][i][k]
    displayImageColor()

# 영상 회전 알고리즘 - 중심, 역방향
def rotateImage2Color() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    angle = askinteger("회전", "값-->", minvalue=1, maxvalue=360)
    ## 중요! 코드. 출력영상 크기 결정 ##
    outH = inH;  outW = inW;
    ###### 메모리 할당 ################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####### 진짜 컴퓨터 비전 알고리즘 #####
    radian = angle * math.pi / 180
    cx = inW//2; cy = inH//2   # (cx, cy)는 중심점.
    for RGB in range(3):
        for i in range(outH) :
            for k in range(outW) :
                xs = i ; ys = k;
                xd = int(math.cos(radian) * (xs-cx) - math.sin(radian) * (ys-cy)) + cx
                yd = int(math.sin(radian) * (xs-cx) + math.cos(radian) * (ys-cy)) + cy
                if 0<= xd < outH and 0 <= yd < outW :
                    outImage[RGB][xs][ys] = inImage[RGB][xd][yd]
                else :
                    outImage[RGB][xs][ys] = 255

    displayImageColor()

# 엠보싱 처리
def embossImageRGB():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    MSIZE = 3
    mask = [ [-1, 0, 0],
             [ 0, 0, 0],
             [ 0, 0, 1] ]

    ## 임시 입력영상 메모리 확보 -> Input 메모리 확보를 위한.
    tmpInImage, tmpOutImage = [], []
    for _ in range(3):
        tmpInImage.append(malloc(inH + (MSIZE - 1), inW + (MSIZE -1), 127))  # 127은 중간값 / 마스크에 따라 바깥 처리를 달리한다.
    for _ in range(3):
        tmpOutImage.append(malloc(outH, outW))
    ## 원 입력 ~~> 임시 입력
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]   # 바깥 쪽 값 입력
    ## 회선연산
    for RGB in range(3):
        for i in range(MSIZE//2, inH + MSIZE//2):   # 큰 틀이 주가 아니라, 더 안쪽의 값이 inputImage임
            for k in range(MSIZE//2, inW + MSIZE//2):
                # 각 점을 처리
                S = 0.0# S는 누적값
                for m in range(0, MSIZE):
                    for n in range(0, MSIZE):
                        S += mask[m][n] * tmpInImage[RGB][i + m - MSIZE//2][k + n - MSIZE//2]
                tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = S
    ## 127 더하기 -> 선택해서 진행.
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                tmpOutImage[RGB][i][k] += 127
    for RGB in range(3):
        ## 임시 출력 --> 원 출력
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[RGB][i][k]
                if value > 255:
                    value = 255
                elif value < 0:
                    value = 0
                outImage[RGB][i][k] = int(value)
    displayImageColor()

def embossImagePillow():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global photo,cvPhoto
    ## 중요! 코드, 출력영상 크기 결정 ##
    photo2 = photo.copy()
    photo2 = photo2.filter(ImageFilter.EMBOSS)
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ############메모리 할당################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    for i in range(outH) :
        for k in range(outW) :
            r, g, b = photo2.getpixel((k,i))   # (163, 58, 73) 형태로 나옴. jpg이기 때문에 기존 raw와는 다르다.
            outImage[R][i][k] = r
            outImage[G][i][k] = g
            outImage[B][i][k] = b
    displayImageColor()

import colorsys
sx, sy, ex, ey = [0] * 4# start, end
def embossImageHSV():  # 마우스 입력 받고 처리를 할 것임. 후에 밑에 __에서 emboss 처리가 진행 될 것임.
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx,sy,ex,ey
    ## 이벤트 바인드
    canvas.bind("<Button-3>", rightMouseClick_embossImageHSV) # <Button-3>은 오른쪽 버튼
    canvas.bind("<Button-1>", leftMouseClick)
    canvas.bind("<B1-Motion>", leftMouseMove)
    canvas.bind("<ButtonRelease-1>", leftMouseDrop_embossImageHSV)
    canvas.configure(cursor='mouse')

def leftMouseDrop_embossImageHSV(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey
    ex = event.x
    ey = event.y
    #####################
    __embossImageHSV()
    #####################
    canvas.unbind("<Button-3>")  # <Button-3>은 오른쪽 버튼
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

boxLine = None
def leftMouseMove(event):
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx,sy,ex,ey, boxLine
    ex = event.x; ey = event.y
    #움직일 때마다 사진이 움직이고, 앞쪽은 지워져야 함.
    if not boxLine:
        pass
    else:
        canvas.delete(boxLine)
    boxLine = canvas.create_rectangle(sx,sy,ex,ey,fill=None)

def leftMouseClick(event):
    global sx,sy,ex,ey
    sx = event.x; sy = event.y

def rightMouseClick_embossImageHSV(event):  # 마우스 오른쪽 버튼 드래그 하면 엠보싱 HSV 처리가 됨.
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global sx, sy, ex, ey
    sx = 0; sy = 0; ex = inH - 1; ey = inW - 1  # 마지막 점까지 인정해주기 위해 -1을 함. 0 ~ inH-1
    #####################
    __embossImageHSV()
    #####################
    canvas.unbind("<Button-3>")  # <Button-3>은 오른쪽 버튼
    canvas.unbind("<Button-1>")
    canvas.unbind("<B1-Motion>")
    canvas.unbind("<ButtonRelease-1>")

def __embossImageHSV():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 입력 RGB --> 입력 HSV
    ## 메모리 확보
    inImageHSV = []
    for _ in range(3):
        inImageHSV.append(malloc(inH, inW))
    #RGB -> HSV
    for i in range(inH):
        for k in range(inW):
            r, g, b  = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
            ## 색상(Hue), 채도(Saturation), 명도(Value)
            ## RGB는 0~255까지 받는데, HSV는 0~1.0까지로 받을 수 있음.
            inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] = h, s, v
            ## h,s,v를 inImageHSV에 저장함.

    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    MSIZE = 3
    mask = [[-1, 0, 0],
            [0, 0, 0],
            [0, 0, 1]]

    ## 임시 입력영상 메모리 확보 -> Input 메모리 확보를 위한.
    tmpInImageV, tmpOutImageV = [], []
    tmpInImageV = (malloc(inH + (MSIZE - 1), inW + (MSIZE - 1), 127))  # 127은 중간값 / 마스크에 따라 바깥 처리를 달리한다.
    tmpOutImageV = (malloc(outH, outW))
    ## 원 입력 ~~> 임시 입력
    for i in range(inH):
        for k in range(inW):
            tmpInImageV[i + MSIZE // 2][k + MSIZE // 2] = inImageHSV[2][i][k]  # 바깥 쪽 값 입력
    ## 회선연산
    for i in range(MSIZE // 2, inH + MSIZE // 2):  # 큰 틀이 주가 아니라, 더 안쪽의 값이 inputImage임
        for k in range(MSIZE // 2, inW + MSIZE // 2):
            # 각 점을 처리
            S = 0.0  # S는 누적값
            for m in range(0, MSIZE):
                for n in range(0, MSIZE):
                    S += mask[m][n] * tmpInImageV[i + m - MSIZE // 2][k + n - MSIZE // 2]
            tmpOutImageV[i - MSIZE // 2][k - MSIZE // 2] = S * 255
    ## 127 더하기 -> 선택해서 진행.
    for i in range(outH):
        for k in range(outW):
            tmpOutImageV[i][k] += 127
            if tmpOutImageV[i][k] > 255:
                tmpOutImageV[i][k] = 255
            elif tmpOutImageV[i][k] < 0:
                tmpOutImageV[i][k] = 0

    ## HSV --> RGB
    for i in range(outH):
        for k in range(outW):
            if sx <= k <= ex and sy <= i <= ey : # 범위에 포함되면
                h, s, v = inImageHSV[0][i][k], inImageHSV[1][i][k], tmpOutImageV[i][k]
                r, g, b = colorsys.hsv_to_rgb(h, s, v)
                outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)
            else:
                outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]

    displayImageColor()

def blurrImageRGB():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    MSIZE = 3
    mask = [ [1/9, 1/9, 1/9],
             [1/9, 1/9, 1/9],
             [1/9, 1/9, 1/9] ]

    ## 임시 입력영상 메모리 확보 -> Input 메모리 확보를 위한.
    tmpInImage, tmpOutImage = [], []
    for _ in range(3):
        tmpInImage.append(malloc(inH + (MSIZE - 1), inW + (MSIZE -1), 127))  # 127은 중간값 / 마스크에 따라 바깥 처리를 달리한다.
    for _ in range(3):
        tmpOutImage.append(malloc(outH, outW))
    ## 원 입력 ~~> 임시 입력
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]   # 바깥 쪽 값 입력
    ## 회선연산
    for RGB in range(3):
        for i in range(MSIZE//2, inH + MSIZE//2):   # 큰 틀이 주가 아니라, 더 안쪽의 값이 inputImage임
            for k in range(MSIZE//2, inW + MSIZE//2):
                # 각 점을 처리
                S = 0.0# S는 누적값
                for m in range(0, MSIZE):
                    for n in range(0, MSIZE):
                        S += mask[m][n] * tmpInImage[RGB][i + m - MSIZE//2][k + n - MSIZE//2]
                tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = S
    for RGB in range(3):
        ## 임시 출력 --> 원 출력
        for i in range(outH):
            for k in range(outW):
                value = tmpOutImage[RGB][i][k]
                if value > 255:
                    value = 255
                elif value < 0:
                    value = 0
                outImage[RGB][i][k] = int(value)
    displayImageColor()
def addSValuePillow():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    global photo,cvPhoto
    ## 중요! 코드, 출력영상 크기 결정 ##
    value = askfloat("", "0-1-10") # 1보다 커지면 채도가 진해지고, ....
    photo2 = photo.copy()
    photo2 = ImageEnhance.Color(photo2)
    photo2 = photo2.enhance(value)

    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ############메모리 할당################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    for i in range(outH) :
        for k in range(outW) :
            r, g, b = photo2.getpixel((k,i))   # (163, 58, 73) 형태로 나옴. jpg이기 때문에 기존 raw와는 다르다.
            outImage[R][i][k] = r
            outImage[G][i][k] = g
            outImage[B][i][k] = b
    displayImageColor()

def addSValueHSV():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 입력 RGB --> 입력 HSV
    ## 메모리 확보
    inImageHSV = []
    for _ in range(3):
        inImageHSV.append(malloc(inH, inW))
    # RGB -> HSV
    for i in range(inH):
        for k in range(inW):
            r, g, b = inImage[R][i][k], inImage[G][i][k], inImage[B][i][k]
            h, s, v = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
            ## 색상(Hue), 채도(Saturation), 명도(Value)
            ## RGB는 0~255까지 받는데, HSV는 0~1.0까지로 받을 수 있음.
            inImageHSV[0][i][k], inImageHSV[1][i][k], inImageHSV[2][i][k] = h, s, v
            ## h,s,v를 inImageHSV에 저장함.

    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    #####메모리 할당##################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ####진짜 컴퓨터 비전 알고리즘 #############
    value = askfloat("", "-255-255")
    value /= 255
    ## HSV --> RGB
    for i in range(outH):
        for k in range(outW):
            newS = inImageHSV[1][i][k] + value
            if newS < 0:  #1이 넘어가면 안됨.
                newS =0
            elif newS > 1.0:
                newS = 1.0
            h, s, v = inImageHSV[0][i][k], newS, inImageHSV[2][i][k] * 255
            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = int(r), int(g), int(b)
    displayImageColor()


# 이진화(=흑백 칼러? 영상)
def bwImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###############메모리 할당####################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    # avg_RGB[][] 만들기 => inImage[R] inImage[G] inImage[B]를 하나로 통합
    avg_RGB = []  # inImage에서 [R], [G], [B]의 평균을 구하기 위함.
    avg_RGB = malloc(inH, inW)
    for i in range(inH):
        for k in range(inW):
            avg_RGB[i][k] = (inImage[R][i][k] + inImage[G][i][k] + inImage[B][i][k]) // 3

    # avg_RGB[][]의 평균 계산.
    sum = 0
    for i in range(inH):
        for k in range(inW):
            sum += avg_RGB[i][k]
    avg = sum // (inH * inW)

    # 이진화 진행 => avg_RGB[][]의 평균 값과 비교
    for i in range(inH):
        for k in range(inW):
            if avg_RGB[i][k] > avg:
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = 255
            else:
                outImage[R][i][k] = outImage[G][i][k] = outImage[B][i][k] = 0

    displayImageColor()

#영상 축소 알고리즘(평균변환)
def zoomOutImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    value = askinteger("축소", "값~~>", minvalue=2, maxvalue=16)  # 최소 1, 최대 255
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH//value
    outW = inW//value
    ###################################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i//value][k//value] += inImage[RGB][i][k]
        for m in range(outH):
            for n in range(outW):
                outImage[RGB][m][n] //= (value*value)
    displayImageColor()

# 영상 확대 알고리즘 (양선형 보간) -> 영상 품질을 향상시킬 수 있음.
def zoomInImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    value = askinteger("확대", "값~~>", minvalue=2, maxvalue=4)  # 최소 1, 최대 255
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH * value
    outW = inW * value
    ###################################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    rH, rW, iH, iW = [0] * 4 # 실수위치 및 정수 위치   / real integer
    x,y = 0, 0 # 실수와 정수의 차이값
    C1,C2,C3,C4 = [0] * 4 # 결정할 위치(N)의 상하좌우 픽셀
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                rH = i / value; rW = k / value    # 확대하기 때문에 나눠야 함.
                iH = int(rH); iW = int(rW)   # 나눈 값을 정수로 나타냄.
                x = rW - iW; y = rH - iH  #
                if 0 <= iH < inH-1 and 0 <= iW < inW-1:
                    C1 = inImage[RGB][iH][iW]
                    C2 = inImage[RGB][iH][iW + 1]
                    C3 = inImage[RGB][iH+1][iW+1]
                    C4 = inImage[RGB][iH+1][iW]
                    newValue = C1*(1-y)*(1-x) + C2*(1-y)*x + C3*y*x + C4*y*(1-x)
                    outImage[RGB][i][k] = int(newValue)
    displayImageColor()


# 히스토그램 -> 영상 그래프를 시각적으로 확인하기 위함.
import matplotlib.pyplot as plt
def histoImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    inCountList = [[0] * 256 for _ in range(3)]  # 3면이기 때문에 0*256 * 3이 되어야 함.
    outCountList = [[0] * 256 for _ in range(3)]

    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                inCountList[RGB][inImage[RGB][i][k]] += 1  # inCountList[0], inCountList[1], inCountList[2] 값을 각각 더해줌.
        for i in range(outH):
            for k in range(outW):
                outCountList[RGB][outImage[RGB][i][k]] += 1

    plt.plot(outCountList[R], 'r-')
    plt.plot(outCountList[G], 'g-')
    plt.plot(outCountList[B], 'b-')
    plt.show()

#히스토그램 -> matplotlib 사용 없이 진행.
def histoImage2Color():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    outCountList = [[0] * 256 for _ in range(3)]
    normalCountList = [[0] * 256 for _ in range(3)]

    #빈도수 계산  -> 이어주는 것이 중요. minVal[]을 만들 필요가 없음.
    for RGB in range(3):
        for i in range(outH):
            for k in range(outW):
                outCountList[RGB][outImage[RGB][i][k]] += 1
        maxVal = max(outCountList[RGB])
        minVal = min(outCountList[RGB])
        High = 256
        # 정규화 = (카운트 값 - 최소값) * High / (최대값 - 최소값)
        for i in range(len(outCountList[RGB])):
            normalCountList[RGB][i] = (outCountList[RGB][i] - minVal) * High / (maxVal - minVal)
    ## 서브 윈도창 생성 후 출력
    subWindow = Toplevel(window) # 그래프가 3개 나와야 하므로, subWindow에서 가로는 곱하기 3을 해주고, 세로는 그대로 놔둔다.
    subWindow.geometry('%dx%d' %(256*3, 256))
    subCanvas = Canvas(subWindow, width=256*3,height = 256)
    subPaper = PhotoImage(width = 256*3, height = 256)
    subCanvas.create_image((256*3//2, 256//2), image = subPaper, state='normal')
    for RGB in range(3):
        for i in range(len(normalCountList[RGB])):   # 255번 돌아감.
            for k in range(int(normalCountList[RGB][i])): # 0 <= normalCountList[i] <= 256
                #data = 0   # data=0으로 해준 이유는 검은색만 나오게 하기 위함.
                if RGB == R:  # RGB 값이 0이면
                    subPaper.put('#d62719', (256 * RGB + i, 255 -k))
                elif RGB == G:
                    subPaper.put('#4fc34e', (256 * RGB + i, 255 -k ))
                elif RGB == B:
                    subPaper.put('#1948b4', (256 * RGB + i, 255-k))
    subCanvas.pack(expand=1, anchor = CENTER)
    subWindow.mainloop()

# 스트레칭 알고리즘
def stretchImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    for RGB in range(3):
        maxVal = minVal = inImage[RGB][0][0]
        for i in range(inH):
            for k in range(inW):
                if inImage[RGB][i][k] < minVal:
                    minVal = inImage[RGB][i][k]
                elif inImage[RGB][i][k] > maxVal:
                    maxVal = inImage[RGB][i][k]
        for i in range(inH):
            for k in range(inW):
                outImage[RGB][i][k] = int(((inImage[RGB][i][k] - minVal) / (maxVal - minVal)) * 255)
    displayImageColor()

#End-in image
def endinImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    minAdd = askinteger("최소", "최소추가~~>", minvalue=0, maxvalue=255)
    maxAdd = askinteger("최대", "최소감소~~>", minvalue=0, maxvalue=255)

    for RGB in range(3):
        maxVal = minVal = inImage[RGB][0][0]
        for i in range(inH):
            for k in range(inW):
                if inImage[RGB][i][k] < minVal:
                    minVal = inImage[RGB][i][k]
                elif inImage[RGB][i][k] > maxVal:
                    maxVal = inImage[RGB][i][k]
        minVal += minAdd
        maxVal -= maxAdd
        for i in range(inH):
            for k in range(inW):
                value = int((inImage[RGB][i][k] - minVal) / (maxVal - minVal)) * 255
                if value <0:
                    value = 0
                elif value >255:
                    value = 255
                outImage[RGB][i][k] = value
    displayImageColor()

# 평활화 - 강사님 방법
def equalizeImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    for RGB in range(3):
        histo = [0] * 256; sumHisto = [0] * 256; normalHisto =[0] * 256  # RGB값이 바뀔 때 마다, 계속 바뀌는 값
        # 1. 빈도 수 조사
        for i in range(inH):
            for k in range(inW):
                histo[inImage[RGB][i][k]] += 1
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
                outImage[RGB][i][k] = normalHisto[inImage[RGB][i][k]]
    displayImageColor()



## 임시 경로에 outImage를 저장하기.
#-> 이미지를 바로 DB에 넣을 수 없기 때문에 파일로 변환하여 DB에 넣는 과정
import random
import struct
def saveTempImage():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    import tempfile
    saveFp = tempfile.gettempdir() + "/" + str(random.randint(10000,99999)) + ".jpg"
    ## .jpg 파일이 겹치지 않도록.
    if saveFp == '' or saveFp == None:
        return
    outArray = []
    for i in range(outH):
        tmpList = []
        for k in range(outW):
            tup = tuple([outImage[R][i][k], outImage[G][i][k], outImage[B][i][k],])
            tmpList.append(tup)
        outArray.append(tmpList)

    outArray = np.array(outArray)
    savePhoto = Image.fromarray(outArray.astype(np.uint8), 'RGB')

    savePhoto.save(saveFp)
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
IP_ADDR = '192.168.56.110'; USER_NAME = 'root'; USER_PASS = '1234'
DB_NAME = 'BigData_DB'; CHAR_SET = 'utf8'
def saveMysqlColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user =USER_NAME, password=USER_PASS,
                          db = DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    try:
        sql = '''
                CREATE TABLE filenameImage_TBL (
                filename_id INT AUTO_INCREMENT PRIMARY KEY,
                filename_fname VARCHAR(30),
                filename_extname CHAR(5),
                filename_height SMALLINT, filename_width SMALLINT,
                filename_avg TINYINT UNSIGNED,
                filename_max TINYINT UNSIGNED, filename_min TINYINT UNSIGNED,
                filename_data LONGBLOB);
        '''
        ## SMALLINT 는 2바이트 / TINYINT는 1바이트 LONGBLOB은 DB에 파일을 저장해놓는 형식
        cur.execute(sql)
    except:
        pass

    ## outImage를 임시 폴더에 저장하고, 이걸 fullname으로 전달.
    fullname = saveTempImage()
    print(type(fullname))
    with open(fullname, 'rb') as rfp:
        binData = rfp.read()

    fname, extname = os.path.basename(fullname).split(".")
    fsize = os.path.getsize(fullname)
    height = width = int(math.sqrt(fsize))
    avgVal, maxVal, minValue = findStat(fullname)  # 평균,최대,최소
    sql = "INSERT INTO filenameImage_TBL(filename_id, filename_fname, filename_extname,"
    sql += "filename_height, filename_width, filename_avg, filename_max, filename_min, filename_data) "
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

def loadMysqlColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    con = pymysql.connect(host=IP_ADDR, user=USER_NAME, password=USER_PASS,
                          db=DB_NAME, charset=CHAR_SET)
    cur = con.cursor()
    sql = "SELECT filename_id, filename_fname, filename_extname, filename_height, filename_width "
    sql += "FROM filenameImage_TBL"
    cur.execute(sql)

    queryList = cur.fetchall()  # 전체 불러오기.
    print(queryList)
    rowList = [':'.join(map(str,file)) for file in queryList]
    import tempfile  # C:\Users\user\AppData\Local\Temp 로 가도록 하는 라이브러리가 tempfile -> 요기에서 조작.
    def selectRecord():
        global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
        selIndex = listbox.curselection()[0]  # 0, 1, 2 ... 순으로 나온다.
        subWindow.destroy()  # 선택을 하면 subWindow 창을 닫는다.
        filename_id = queryList[selIndex][0]
        sql = "SELECT filename_fname, filename_extname, filename_data FROM filenameImage_TBL "
        sql += "WHERE filename_id = " + str(filename_id)
        cur.execute(sql)   # 이 줄부터 위 두 줄은 이미지에서 필요한 것들만 가져옴.
        fname, extname, binData = cur.fetchone()
        print()
        fullPath = tempfile.gettempdir() + '/' + fname + "." + extname # C:\Users\user\AppData\Local\Temp/64319.raw 형태로 저장.
        with open(fullPath, 'wb') as wfp:  # 이 과정을 진행하지 않으면 펜은 있는데 종이는 없는 느낌. with문 과정이 반드시 필요. 후에 뒤에서 삭제를 해줘야 함.
            wfp.write(binData)            #
        cur.close()
        con.close()
        print(tempfile)
        print(fullPath)

        loadImageColor(fullPath)   # 메모리에 적재만 되었고 equalImage에서 display가 된다.
        equalImageColor()
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
    for _ in range(3):
        inImage.append(malloc(inH, inW))   # 면을 3개 만든다.
    #파일 --> 메모리
    with open(fname, 'r') as rFp:
        for row_list in rFp:
            row, col, rValue, gValue, bValue  = list(map(int, row_list.strip().split(",")))
            inImage[R][row][col] = rValue
            inImage[G][row][col] = gValue
            inImage[B][row][col] = bValue

def openCSVColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    filename = askopenfilename(parent = window,
            filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if filename == '' or filename == None:
        return
    loadCSV(filename)
    equalImageColor()

import csv
def saveCSVColor():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    saveFp = asksaveasfile(parent=window, mode='wb',
                           defaultextension='*.csv', filetypes=(("CSV 파일", "*.csv"), ("모든 파일", "*.*")))
    if saveFp == "" or saveFp == None:
        return
    with open(saveFp.name, 'w', newline='') as wFp:
        csvWriter = csv.writer(wFp)
        for i in range(outH):
            for k in range(outW):
                row_list = [i, k, outImage[R][i][k], outImage[G][i][k], outImage[B][i][k]]
                csvWriter.writerow(row_list)
    print("CSV.save OK~")

import xlwt
def saveExcelColor():
    pass

################################################
## OpenCV 용 컴퓨터 비전/딥러닝
################################################
def toColorOutArray(pillowPhoto):
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ################메모리 할당######################
    outH = pillowPhoto.height; outW = pillowPhoto.width
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    photoRGB = pillowPhoto.convert('RGB')
    for i in range(outH):
        for k in range(outW):
            r,g,b = photoRGB.getpixel((k, i))
            outImage[R][i][k], outImage[G][i][k], outImage[B][i][k] = r,g,b

    displayImageColor()

def embossOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    cvPhoto2 = cvPhoto[:]
    mask = np.zeros((3,3), np.float32)
    mask[0][0] = -1; mask[2][2] = 1
    cvPhoto2 = cv2.filter2D(cvPhoto2, -1, mask)
    cvPhoto2 += 127
    photo2 = Image.fromarray(cvPhoto2)
    toColorOutArray(photo2) # PIL 을 outIamge에 출력.

def grayscaleOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2) # PIL 을 outIamge에 출력.

def blurOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    mSize = askinteger("블러링", "마스크 크기 : ")
    cvPhoto2 = cvPhoto[:]
    mask = np.ones((mSize, mSize), np.float32) / (mSize*mSize)
    cvPhoto2 = cv2.filter2D(cvPhoto2, -1, mask)
    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2) # PIL 을 outIamge에 출력.

def rotateOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    angle = askinteger("회전", "각도 : ")
    cvPhoto2 = cvPhoto[:]
    rotate_matrix = cv2.getRotationMatrix2D((outW//2, outH//2), angle, 1 ) # 중앙점, 각도, 스케일(확대)
    cvPhoto2 = cv2.warpAffine(cvPhoto2, rotate_matrix, (outH, outW))
    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2)  # PIL 을 outIamge에 출력.

def zoomInOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    scale = askinteger("확대", "배수 : ")
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.resize(cvPhoto2, None, fx=scale, fy = scale)
    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2)  # PIL 을 outIamge에 출력.


def waveHorOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    cvPhoto2 = np.zeros(cvPhoto.shape, dtype=cvPhoto.dtype)
    for i in range(inH):
        for k in range(inW):
            oy = int(15.0 * math.sin(2*3.14*k / 180))
            ox = 0
            if i + oy < inH:
                cvPhoto2[i][k] = cvPhoto[(i+oy) % inH][k]
            else:
                cvPhoto2[i][k] = 0
    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2)  # PIL 을 outIamge에 출력.

def waveVirOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    cvPhoto2 = np.zeros(cvPhoto.shape, dtype=cvPhoto.dtype)
    for i in range(inH):
        for k in range(inW):
            ox = int(25.0 * math.sin(2 * 3.14 * i / 180))
            oy = 0
            if k + ox < inW:
                cvPhoto2[i][k] = cvPhoto[i][(k + ox) % inW]
            else:
                cvPhoto2[i][k] = 0
    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2)  # PIL 을 outIamge에 출력.

def cartoonOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    cvPhoto2 = cv2.medianBlur(cvPhoto2, 7)
    edges = cv2.Laplacian(cvPhoto2, cv2.CV_8U, ksize=5)
    ret, mask = cv2.threshold(edges, 100, 255, cv2.THRESH_BINARY_INV)
    cvPhoto2 = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2)  # PIL 을 outIamge에 출력.


# https://076923.github.io/posts/Python-opencv-14/ 참고
def cannyOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    cvPhoto2 = cvPhoto[:]
    cvPhoto2 = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    canny = cv2.Canny(cvPhoto2, 100, 255)
    ## cv2.Canny(원본 이미지, 임계값1, 임계값2) => 가장자리 검출
    sobel = cv2.Sobel(canny, cv2.CV_8U, 1, 0, 3)
    ## cv2.Sobel(그레이스케일 이미지, 정밀도, x방향 미분, y방향 미분, 커널...)
    cvPhoto2 = cv2.Laplacian(cvPhoto2, cv2.CV_8U, ksize=3)
    ## cv.Laplacian(그레이스케일 이미지, 정밀도, 커널) ...
    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2)  # PIL 을 outIamge에 출력.

# XML은 얼굴 인식 학습을 미리 시킨 파일임. 안에 보면 숫자들이 저장되어 있음.
def faceDetectOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    face_cascade = cv2.CascadeClassifier("C:/BigData/haar/haarcascade_frontalface_alt.xml")
    cvPhoto2 = cvPhoto[:]
    gray = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)
    ## 얼굴찾기
    face_rects = face_cascade.detectMultiScale(gray, 1.1, 5)  # 파라미터 조절 가능.
    for (x, y, w, h) in face_rects:
        cv2.rectangle(cvPhoto2, (x, y), (x + w, y + w), (0, 255, 0), 3)

    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2)  # PIL 을 outIamge에 출력.

# overlap - 한니발 이미지를 불러와서 사람들 이미지에 씌움.
def hanibalOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    face_cascade = cv2.CascadeClassifier("C:/BigData/haar/haarcascade_frontalface_alt.xml")
    faceMask = cv2.imread("C:/images/images(ML)/mask_hannibal.png")
    h_mask, w_mask = faceMask.shape[:2]
    cvPhoto2 = cvPhoto[:]
    gray = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴찾기 - 마스크 얼굴이랑 원래 얼굴이랑 겹쳐서 풀링 효과를 내기 위함.
    face_rects = face_cascade.detectMultiScale(gray, 1.1, 5)  # 파라미터 조절 가능.
    for (x, y, w, h) in face_rects:
        if h > 0 and w > 0:
            x = int(x+0.1*w); y = int(y+0.4*h)
            w = int(0.8 * w); h = int(0.8*h)
            cvPhoto2_2 = cvPhoto2[y:y+h, x:x+w]
            faceMask_samll = cv2.resize(faceMask, (w,h), interpolation=cv2.INTER_AREA)
            gray_mask = cv2.cvtColor(faceMask_samll, cv2.COLOR_RGB2GRAY)
            ret, mask = cv2.threshold(gray_mask, 50, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            maskedFace = cv2.bitwise_and(faceMask_samll, faceMask_samll, mask = mask)
            maskedFrame = cv2.bitwise_and(cvPhoto2_2, cvPhoto2_2, mask_inv)
            cvPhoto2[y:y+h, x:x+w] = cv2.add(maskedFace, maskedFrame)
    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2)  # PIL 을 outIamge에 출력.


def sunglassOpenCV():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    global photo, cvPhoto
    if inImage == None:
        return
    ############이 부분이 OpenCV 처리 부분############################################
    face_cascade = cv2.CascadeClassifier("C:/BigData/haar/haarcascade_frontalface_alt.xml")
    faceMask = cv2.imread("C:/images/MyPicture/sunglass.png")
    h_mask, w_mask = faceMask.shape[:2]
    cvPhoto2 = cvPhoto[:]
    gray = cv2.cvtColor(cvPhoto2, cv2.COLOR_RGB2GRAY)

    ## 얼굴찾기 - 마스크 얼굴이랑 원래 얼굴이랑 겹쳐서 풀링 효과를 내기 위함.
    face_rects = face_cascade.detectMultiScale(gray, 1.1, 5)  # 파라미터 조절 가능.
    for (x, y, w, h) in face_rects:
        if h > 0 and w > 0:
            x = int(x+0.1*w); y = int(y+0.4*h)
            w = int(0.8 * w); h = int(0.8*h)
            cvPhoto2_2 = cvPhoto2[y:y+h, x:x+w]
            faceMask_samll = cv2.resize(faceMask, (w,h), interpolation=cv2.INTER_AREA)
            gray_mask = cv2.cvtColor(faceMask_samll, cv2.COLOR_RGB2GRAY)
            ret, mask = cv2.threshold(gray_mask, 50, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask)
            maskedFace = cv2.bitwise_and(faceMask_samll, faceMask_samll, mask = mask)
            maskedFrame = cv2.bitwise_and(cvPhoto2_2, cvPhoto2_2, mask_inv)
            cvPhoto2[y:y+h, x:x+w] = cv2.add(maskedFace, maskedFrame)
    photo2 = Image.fromarray(cvPhoto2)
    #########################################################
    toColorOutArray(photo2)  # PIL 을 outIamge에 출력.

####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2
inImage, outImage = [], []  # 3차원 리스트(배열)
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)
####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝-칼라) ver 0.1")

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

## 마우스 이벤트

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImageColor)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImageColor)
comVisionMenu1.add_command(label="반전하기", command=revImageColor)
comVisionMenu1.add_command(label="파라볼라", command=paraImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="모핑", command=morphImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="채도조절(Pillow)", command=addSValuePillow)
comVisionMenu1.add_command(label="채도조절(HSV)", command=addSValueHSV)

comVisionMenu2 = Menu(mainMenu)
mainMenu.add_cascade(label="통계", menu=comVisionMenu2)
comVisionMenu2.add_command(label="이진화", command=bwImageColor)
comVisionMenu2.add_command(label="축소(평균변환)", command=zoomOutImage2Color)
comVisionMenu2.add_command(label="확대(양선형보간)", command=zoomInImage2Color)
comVisionMenu2.add_separator()
comVisionMenu2.add_command(label="히스토그램", command=histoImageColor)
comVisionMenu2.add_command(label="히스토그램(내꺼)", command=histoImage2Color)
comVisionMenu2.add_command(label="명암대비", command=stretchImageColor)
comVisionMenu2.add_command(label="End-In탐색", command=endinImageColor)
comVisionMenu2.add_command(label="평활화", command=equalizeImageColor)

comVisionMenu3 = Menu(mainMenu)
mainMenu.add_cascade(label="기하학 처리", menu=comVisionMenu3)
comVisionMenu3.add_command(label="상하반전", command=upDownImageColor)
comVisionMenu3.add_command(label="이동", command=moveImageColor)
comVisionMenu3.add_command(label="축소", command=zoomOutImageColor)
comVisionMenu3.add_command(label="확대", command=zoomInImageColor)
comVisionMenu3.add_command(label="회전1", command=rotateImageColor)
comVisionMenu3.add_command(label="회전2(중심,역방향)", command=rotateImage2Color)

comVisionMenu4 = Menu(mainMenu)
mainMenu.add_cascade(label="화소영역 처리", menu=comVisionMenu4)
comVisionMenu4.add_command(label="엠보싱(RGB)", command=embossImageRGB)
comVisionMenu4.add_command(label="엠보싱(Pillow제공)", command=embossImagePillow)
comVisionMenu4.add_command(label="엠보싱(HSV)", command=embossImageHSV)
comVisionMenu4.add_separator()
comVisionMenu4.add_command(label="블러링(RGB)", command=blurrImageRGB)

comVisionMenu5 = Menu(mainMenu)
mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysqlColor)
comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysqlColor)
comVisionMenu5.add_separator()
comVisionMenu5.add_command(label="CSV 열기", command=openCSVColor)
comVisionMenu5.add_command(label="CSV로 저장", command=saveCSVColor)
comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label="엑셀 열기", command=openExcel)
comVisionMenu5.add_command(label="엑셀로 저장", command=saveExcelColor)
# comVisionMenu5.add_command(label="엑셀 아트로 저장", command=saveExcelArt)

openCVMenu = Menu(mainMenu)
mainMenu.add_cascade(label="openCV 딥러닝", menu=openCVMenu)
openCVMenu.add_command(label="엠보싱(OpenCV)", command=embossOpenCV)
openCVMenu.add_command(label="그레이스케일(OpenCV)", command=grayscaleOpenCV)
openCVMenu.add_command(label="블러링(OpenCV)", command=blurOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="회전", command=rotateOpenCV)
openCVMenu.add_command(label="확대", command=zoomInOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="수평 웨이브", command=waveHorOpenCV)
openCVMenu.add_command(label="수직 웨이브", command=waveVirOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="카툰화", command=cartoonOpenCV)
openCVMenu.add_command(label="가장자리 이미지 검출", command=cannyOpenCV)
openCVMenu.add_separator()
openCVMenu.add_command(label="얼굴인식(머신러닝)", command=faceDetectOpenCV)
openCVMenu.add_command(label="한니발 마스크(머신러닝)", command=hanibalOpenCV)
openCVMenu.add_command(label="선글라스(머신러닝)", command=sunglassOpenCV)

window.mainloop()



