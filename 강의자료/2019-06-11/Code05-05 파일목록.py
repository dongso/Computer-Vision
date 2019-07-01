import os

for dirName, subDirList, fnames in os.walk("C:/images/"):
    ##dirName은 images 폴더 바로 밑에 폴더를 값으로 불러옴.
    ##subDirList는 images 폴더 안에 폴더(ex - 'Etc_JPG')들의 이름들을 불러옴
    ##fnames는 filename으로, 파일명을 의미함.
    for fname in fnames:
        if os.path.splitext(fname)[1].upper() == ".GIF":
            print(os.path.join(dirName, fname))

## images 폴더 밑 파일들을 다 긁어서 불러온다.
## splitext를 해야 확장명까지...


# 참고1 -> 이거 돌려보면 이해하기 쉬울 것임.
# print(os.walk("C:/images/"))
# for dirName, subDirList, fnames in os.walk("C:/images/"):
#     print(dirName)
#     print("---------")
#     print(subDirList)
#     print("---------")
#     print(fnames)

# 참고2
# for dirName, subDirList, fnames in os.walk("C:/images/"):
#     for fname in fnames:
#         print(os.path.splitext(fname))

# 참고3
# for dirName, subDirList, fnames in os.walk("C:/images/"):
#     for fname in fnames:
#         if os.path.splitext(fname)[1].upper() == ".GIF":
#             print(dirName)
#             print(fname)
