#퀴즈2. Python 에서 아이디, 주민번호, 이메일을 키보드로 입력받은 후,
#데이터베이스에서 저장하기. 아이디를 그냥 엔터치면 그만 입력.

import pymysql

IP = "192.168.56.108"
USER = 'root'
PASS = '1234'
DB = 'quiz_db'
PORT = '3306'

try :
    conn = pymysql.connect(host = IP, user = USER, password = PASS,
                        db = DB, charset="utf8")  # 1. DB 연결 - 트럭만 지음.
    print("연결완료")
except :
    print("DB 연결 실패")
    exit()

cur = conn.cursor()

id = input()
number = input()
email = input()
sql = "INSERT INTO quiz_tbl(quiz_id, quiz_number, quiz_email)"
sql += " VALUES " + "( '" + id + "', '"  + number +"', '" + email +"')"
print(sql)
try :
    cur.execute(sql)
except :
    print("입력 실패 -- 확인요망..")

conn.commit()   # commit을 꼭 해라!!!!!!!!!!!!!!!!!!!!!!!! / commit은 변경했을 때 진행.
cur.close()
conn.close()