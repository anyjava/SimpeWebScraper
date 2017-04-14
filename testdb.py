import sqlite3

# SQLite DB 연결
conn = sqlite3.connect("test.db")
 
# Connection 으로부터 Cursor 생성
cur = conn.cursor()
 
# SQL 쿼리 실행
cur.execute("select * from magnet_list")
 
# 데이타 Fetch
rows = cur.fetchall()
for row in rows:
    print(row[1])
 
# Connection 닫기
conn.close()
