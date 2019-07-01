import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier("C:/BigData/haar/haarcascade_frontalface_alt.xml")

frame = cv2.imread("C:/images/images(ML)/input_fundmatrixL.jpg")# frame은 장면
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
# 얼굴이 여러개일 경우엔 여러개를 찾아줌. 얼굴 위치 사각형 [ [x1,y1,x2,y2], [x1,y1,x2,y2] ... ]
face_rects = face_cascade.detectMultiScale(gray, 1.1, 5) # 파라미터 조절 가능.
for (x,y,w,h) in face_rects:
    cv2.rectangle(frame, (x,y), (x+w, y+w), (0, 255, 0), 3)
cv2.imshow('', frame)
c = cv2.waitKey()
cv2.destroyAllWindows()