# 퀴즈3. 퀴즈2의 데이터베이스를 조회해서 예쁘게 출력.
#       아이디      주민번호      이메일
#      ------------------------------------
#        asjd     00000-0000      dsadf@naver.com


# 조회
import pymysql

# 아이디, 비번, ip 주소, 포트 번호, 까지 알아야 함.

#DB 접속 정보
IP = "192.168.56.108"
USER = 'root'
PASS = '1234'
DB = 'quiz_db'
PORT = '3306'
conn = pymysql.connect(host = IP, user = USER, password = PASS,
                    db = DB, charset="utf8")  # 1. DB 연결 - 트럭만 지음.

cur = conn.cursor()

sql = "SELECT quiz_id, quiz_number, quiz_email FROM quiz_tbl"
cur.execute(sql)


print("아이디 주민번호 이메일")
print("---------------------")
while True :  # 데이터를 메모리로 하나씩 가져옴.
    row = cur.fetchone()
    if row is None:
        break
    print(row[0], row[1], row[2])

cur.close()
conn.close()

