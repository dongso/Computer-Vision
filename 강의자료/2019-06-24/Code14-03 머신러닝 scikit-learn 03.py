from sklearn import svm,metrics
import pandas as pd

##훈련데이터, 테스트데이터 준비
csv = pd.read_csv('c:/bigdata/iris.csv')
train_data = csv.iloc[:, 0:-1]
train_label =csv.iloc[:,[-1]]

#1. Classifire 생성(선택) --> 머신러닝 알고리즘 선택
clf=svm.SVC(gamma='auto')

#2. 데이터로 학습시키기 - XOR에 대한 데이터
#clf.fit([훈련데이터],[정답])
# 훈련 데이터와 테스트 데이터는 대체적으로 8:2, 7:3으로 분류한다.
clf.fit(train_data,train_label)

#3. 정답률을 확인 (신뢰도)
result = clf.predict( [[4.1, 3.3, 1.5, 0.2]])
print(result)