import sqlite3
import subprocess

# SQLite DB 연결
conn = sqlite3.connect("test.db")
 
# Connection 으로부터 Cursor 생성
cur = conn.cursor()
 
# SQL 쿼리 실행
cur.execute("""SELECT a.id
                    , b.title
                 FROM download as a
                 JOIN magnet_list as b ON b.id = a.magnet_id
                WHERE delete_yn = 'N' 
                  AND reg_datetime < DATE('now', '-7 days') 
                """)
 
# 데이타 Fetch
rows = cur.fetchall()
for row in rows:
    download_id = row[0]
    title = row[1]
    subprocess.call('/home/anyjava/_dev/scrapMagnet/delete.sh "' + title + '"', shell=True)
    cur.execute("UPDATE download SET delete_yn = 'Y' WHERE id = ?", (download_id,))
    conn.commit()
    

# Connection 닫기
conn.close()
