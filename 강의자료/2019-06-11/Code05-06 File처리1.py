#1. 파일 열기
inFp = open("C:/windows/win.ini", "r")
outFp = open("C:/images/new_win.ini", "w")
## ini 파일은 일반 글자가 쓰여있는 텍스트 파일
## rt는 read textmode
#2. 파일 읽기/쓰기
while True:
    inStr = inFp.readline()
    if not inStr: # 아무것도 없으면
        break
    outFp.writelines(inStr)

# inStrList = inFp.readlines()
# print(inStrList)
# for line in inStrList:
#     print(line, end='')

#print(inStr, end ='')
#inStr = inFp.readline()
#print(inStr, end ='')
#inStr = inFp.readline()
#print(inStr, end ='')
#3. 파일 닫기
inFp.close()
outFp.close()
print("ok")