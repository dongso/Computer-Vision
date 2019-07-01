import pandas as pd
from sklearn import svm, metrics
'''
# 붗꽃 데이터 분류기(머신러닝)
- 개요 : 150개 붗꽃 정보(꽃받침 길이, 꽃받침 폭, 꽃잎 길이, 꽃잎 폭)
- 종류 : 3개 (Iris-setosa, Iris-vesicolor, Iris-virginica)
- CSV 파일 : 검색 iris.csv
'''
##0. 훈련데이터, 테스트데이터 준비
csv = pd.read_csv("C:/BigData/iris.csv")
train_data = csv.iloc[0:120, 0:-1]
train_label = csv.iloc[0:120, [-1]]
test_data = csv.iloc[120:, 0:-1]
test_label = csv.iloc[120:, [-1]]
#1. Classifier 생성(선택) --> 머신러닝 알고리즘 선택
clf = svm.SVC(gamma="auto")  # clf는 classifier의 약자
#2. 데이터로 학습 시키기
#clf.fit( [ 훈련데이터 ], [ 정답 ])
clf.fit (train_data, train_label)
#3. 정답률을 확인(신뢰도)
results = clf.predict(test_data)
score = metrics.accuracy_score(results, test_label)
print("정답률 :" , score*100 , '%')

#4. 내꺼 예측하기
result = clf.predict([[4.1, 3.3, 1.5, 0.2]])
print(result)