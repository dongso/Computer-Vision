from sklearn import svm, metrics

##0. 훈련데이터, 테스트데이터 준비
train_data = [[0,0],[0,1],[1,0],[1,1]]
train_label = [0,1,1,0]
test_data = [[1, 0], [0, 0]]
test_label = [1,0]

#1. Classifier 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.NuSVC(gamma = "scale")  # clf는 classifier의 약자
#2. 데이터로 학습 시키기
#clf.fit( [ 훈련데이터 ], [ 정답 ])
clf.fit (train_data, train_label)
#3. 정답률을 확인(신뢰도)
results = clf.predict(test_data)
score = metrics.accuracy_score(results, test_label)
print("정답률 :", score*100, '%')
