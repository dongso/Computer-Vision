# And 게이트를 훈련시키고 결과를 보자

from sklearn import svm

#1. Classifier 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.SVC(gamma = "scale")  # clf는 classifier의 약자

#2. 데이터로 학습 시키기
#clf.fit( [ 훈련데이터 ], [ 정답 ])
clf.fit ( [ [0,0],
            [0,1],
            [1,0],
            [1,1]],
          [0,0,0,1])
#3. 예측하기
# clf.predict( [예측할 데이터] )
result1 = clf.predict( [ [0,0] ])
result2 = clf.predict( [ [0,1] ])
result3 = clf.predict( [ [1,0] ])
result4 = clf.predict( [ [1,1] ])

print(result1, result2, result3, result4)
