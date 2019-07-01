from sklearn import svm, metrics

#1. Classifier 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.SVC(gamma = "scale")  # clf는 classifier의 약자

#2. 데이터로 학습 시키기
#clf.fit( [ 훈련데이터 ], [ 정답 ])
clf.fit ( [ [0,0],
            [0,1],
            [1,0],
            [1,1]],
          [0,1,1,0])

#3. 예측
results = clf.predict([[1, 0], [0, 0]])

#4. 정답률을 확인 (신뢰도)
#
score = metrics.accuracy_score(results, [1,0])

print("정답률 :", score*100, '%')

