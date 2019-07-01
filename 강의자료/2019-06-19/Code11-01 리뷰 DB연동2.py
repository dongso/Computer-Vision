# 조회
import pymysql

# 아이디, 비번, ip 주소, 포트 번호, 까지 알아야 함.

#DB 접속 정보
IP = "192.168.56.108"
USER = 'root'
PASS = '1234'
DB = 'review_db'
PORT = '3306'
conn = pymysql.connect(host = IP, user = USER, password = PASS,
                    db = DB, charset="utf8")  # 1. DB 연결 - 트럭만 지음.

cur = conn.cursor()
sql = "SELECT emp_id, emp_name, emp_pay FROM emp_tbl"
cur.execute(sql)

# 위험한 방법 - 한 번에 가져옴.
# rows = cur.fetchall()  # 한꺼번에 다 갖고와라. 이건 엄청 위험함. 데이터를 메모리로 가져옴.
# for row in rows:
#     print(row[0], row[1], row[2])

# 괜찮은 방법 - 하나씩 가져옴.

while True :  # 데이터를 메모리로 하나씩 가져옴.
    row = cur.fetchone()
    if row is None:
        break
    print(row[0], row[1], row[2])

cur.close()
conn.close()

