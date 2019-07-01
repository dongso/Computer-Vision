# 삽입
import pymysql

# 아이디, 비번, ip 주소, 포트 번호, 까지 알아야 함.

#DB 접속 정보
IP = "192.168.56.108"
USER = 'root'
PASS = '1234'
DB = 'review_db'
PORT = '3306'

try :
    conn = pymysql.connect(host = IP, user = USER, password = PASS,
                        db = DB, charset="utf8")  # 1. DB 연결 - 트럭만 지음.
except :
    print("DB 연결 실패")
    exit()

cur = conn.cursor()
sql = "INSERT INTO emp_tbl(emp_id, emp_name, emp_pay)"
sql +=	" VALUES (10003, N'이순신', 4000)"   # N은 모든 문자열이 입력 되도록 함.

try :
    cur.execute(sql)
except :
    print("입력 실패 -- 확인요망..")

conn.commit()   # commit을 꼭 해라!!!!!!!!!!!!!!!!!!!!!!!! / commit은 변경했을 때 진행.
cur.close()
conn.close()