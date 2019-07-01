import operator

ttL = [('토마스', 5), ('헨리', 8), ('에드워드', 9), ('토마스',12),
       ('에드워드',1)]
tD = {}
tL = []
tR, cR = 1, 1

for tmpTup in ttL:
    tName = tmpTup[0]
    tWeight = tmpTup[1]
    if tName in tD:
        tD[tName] += tWeight
    else:
        tD[tName] = tWeight
##설명
#처음에는 else로 진입, 빈 공간 tD에 (tName, tWeight) 값을 채워준다.
#tName이 이미 존재하면, 같은 tName에 tWeight 값만 더해준다.
print(tD)
print(list(tD.items()))

tL = sorted(tD.items(), key = operator.itemgetter(1), reverse=True)
##설명
#operator 기능 중 하나는 key or values 값에서 정렬을 하기 위함.
#tD를 정렬하는데, itemgetter 별로 정렬하라. itemgetter(1)이기 때문에 values 순으로 정렬을 한다.
#cf. imtemgetter(0)을 하면, key값을 의미하므로, 알파벳 순서로 정렬 됨.
#reverse=True 이므로, values가 내림차순으로 정렬됨.
print(tL)