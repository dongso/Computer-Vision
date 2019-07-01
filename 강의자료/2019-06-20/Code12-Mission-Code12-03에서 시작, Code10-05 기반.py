from tkinter import *
from tkinter.simpledialog import *
from tkinter.filedialog import *
import math
import os
import os.path
from PIL import Image, ImageFilter, ImageEnhance, ImageOps
import time
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
def loadImageColor(fname) :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    inImage = []
    photo = Image.open(fname) # PIL 객체
    inW = photo.width; inH=photo.height
    ## 메모리 확보
    for _ in range(3) :  # 3면 확보
        inImage.append(malloc(inH, inW))
    photoRGB = photo.convert('RGB')   # RGB색을 만들기 위함.
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
    loadImageColor(filename)
    equalImageColor()

def displayImageColor() :
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    if canvas != None : # 예전에 실행한 적이 있다.
        canvas.destroy()
    VIEW_X = outW;    VIEW_Y = outH;   step = 1

    window.geometry(str(int(VIEW_X*1.2)) + 'x' + str(int(VIEW_Y*1.2)))  # 벽 - 여유 분 남기기 위함.
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
            ## equalImage / addImageColor .... 등에서 outImage[0][][], outImage[1][][], outImage[2][][]가 이미 저장되어 있음.
            ##현재 R,G,B는 전역변수로 0, 1, 2로 지정해주었기 때문에 앞에서 저장해놓은 outImage[][][]를 불러올 수 있는 것이다.
            ##그 값을 r,g,b에 대입.
            tmpStr += ' #%02x%02x%02x' % (r,g,b)
        rgbStr += '{' + tmpStr + '} '
    paper.put(rgbStr)

    canvas.bind("<Button-1>", mouseClick)
    canvas.bind("<ButtonRelease-1>", mouseDrop)
    canvas.pack(expand=1, anchor=CENTER)
    status.configure(text='이미지 정보:' + str(outW) + 'x' + str(outH))

def saveImagePIL():
    global window, canvas, paper, filename, inImage, outImage, inH, inW, outH, outW
    # if outImage == None :
    #     return
    # saveFp = asksaveasfile(parent=window, mode='wb',
    #                        defaultextension='*.jpg', filetypes=(("JPG 파일", "*.jpg"), ("모든 파일", "*.*")))
    # if saveFp == '' or saveFp == None:
    #     return
    # outImage.save(saveFp.name)
    # print('Save~')

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
    outImage = []
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

# 이진화(=흑백 칼러? 영상)
def bwImageColor():
    global window, canvas, paper, filename, inImage, outImage, inW, inH, outW, outH
    ## 중요! 코드, 출력영상 크기 결정 ##
    outH = inH;
    outW = inW
    ###################################
    outImage = []
    for _ in range(3):
        outImage.append(malloc(outH, outW))
    ########진짜 컴퓨터 비전 알고리즘 ########
    # 평균을 기준으로 잡자.
    sum = []  # sum 리스트의 원소가 3개 나올 것임. Raw와 달리, 면이 3개인 것이지...
    for RGB in range(3):
        sum.append(0)   # sum의 값 초기화를 시켜줘야 한다.
        for i in range(inH):
            for k in range(inW):
                sum[RGB] += inImage[RGB][i][k]
    avg = [s // (inW * inH) for s in sum] # 평균도 3개가 나옴.
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                if inImage[RGB][i][k] > avg[RGB]:
                    outImage[RGB][i][k] = 255
                else:
                    outImage[RGB][i][k] = 0
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
        for i in range(outH):
            for k in range(outW):
                outImage[RGB][i][k] //= (value*value)
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
def zoomInImageColor() :
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
def embossImageColor():
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
    tmpInImage = []
    tmpOutImage = []
    for _ in range(3):
        tmpInImage.append(malloc(inH + (MSIZE -1), inW + (MSIZE-1), 127))  # 127은 중간값 / 마스크에 따라 바깥 처리를 달리한다.
        tmpOutImage.append(malloc(outH, outW))
    ## 원 입력 ~~> 임시 입력
    for RGB in range(3):
        for i in range(inH):
            for k in range(inW):
                tmpInImage[RGB][i+MSIZE//2][k+MSIZE//2] = inImage[RGB][i][k]   # 바깥 쪽 값 입력

        ## 회선연산
        for i in range(MSIZE//2, inH + MSIZE//2):   # 큰 틀이 주가 아니라, 더 안쪽의 값이 inputImage임
            for k in range(MSIZE//2, inW + MSIZE//2):
                # 각 점을 처리
                S = 0.0# S는 누적값
                for m in range(0, MSIZE):
                    for n in range(0, MSIZE):
                        S += mask[m][n] * tmpInImage[RGB][i + m - MSIZE//2][k + n - MSIZE//2]
                tmpOutImage[RGB][i-MSIZE//2][k-MSIZE//2] = S
        ## 127 더하기 -> 선택해서 진행.
        for i in range(outH):
            for k in range(outW):
                tmpOutImage[RGB][i][k] += 127
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



####################
#### 전역변수 선언부 ####
####################
R, G, B = 0, 1, 2
inImage, outImage = [], []  # 3차원 리스트(배열)
inH, inW, outH, outW = [0] * 4
window, canvas, paper = None, None, None
filename = ""
VIEW_X, VIEW_Y = 512, 512 # 화면에 보일 크기 (출력용)
panYN = False
####################
#### 메인 코드부 ####
####################
window = Tk()
window.geometry("500x500")
window.title("컴퓨터 비전(딥러닝) ver 0.01")

status = Label(window, text='이미지 정보:', bd=1, relief=SUNKEN, anchor=W)
status.pack(side=BOTTOM, fill=X)

## 마우스 이벤트
window.bind("")

mainMenu = Menu(window)
window.config(menu=mainMenu)

fileMenu = Menu(mainMenu)
mainMenu.add_cascade(label="파일", menu=fileMenu)
fileMenu.add_command(label="파일 열기", command=openImageColor)
fileMenu.add_separator()
fileMenu.add_command(label="파일 저장", command=saveImagePIL)

comVisionMenu1 = Menu(mainMenu)
mainMenu.add_cascade(label="화소점 처리", menu=comVisionMenu1)
comVisionMenu1.add_command(label="덧셈/뺄셈", command=addImageColor)
comVisionMenu1.add_command(label="반전하기", command=revImageColor)
comVisionMenu1.add_command(label="파라볼라", command=paraImageColor)
comVisionMenu1.add_separator()
comVisionMenu1.add_command(label="모핑", command=morphImageColor)

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
comVisionMenu4.add_command(label="엠보싱", command=embossImageColor)
#
# comVisionMenu5 = Menu(mainMenu)
# mainMenu.add_cascade(label="기타 입출력", menu=comVisionMenu5)
# comVisionMenu5.add_command(label="MySQL에서 불러오기", command=loadMysql)
# comVisionMenu5.add_command(label="MySQL에 저장하기", command=saveMysql)
# comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label="CSV 열기", command=openCSV)
# comVisionMenu5.add_command(label="CSV로 저장", command=saveCSV)
# comVisionMenu5.add_separator()
# comVisionMenu5.add_command(label="엑셀 열기", command=openExcel)
# comVisionMenu5.add_command(label="엑셀로 저장", command=saveExcel)
# comVisionMenu5.add_command(label="엑셀 아트로 저장", command=saveExcelArt)

window.mainloop()