import sqlite3
import subprocess
from datetime import timedelta, date

TORRENT_HOST = "http://www.tfreeca22.com/"
# SQLite DB 연결
conn = sqlite3.connect("test.db")

class Program:

	def __init__(self, id, title, day_of_week, search_key):
		self.id    = id
		self.title = title
		self.day_of_week  = day_of_week
		self.search_key = search_key
		self.torrent_id = ""
		self.magnet = ""

	def getShowDateOnThisWeek(self):
		return str(self.__calcShowDate()).replace("-", "")[2:]

	def __calcShowDate(self):
		today = date.today()
		weekdayToday = today.isoweekday()

		if (weekdayToday == self.day_of_week):
			return today
		is_prev_week = weekdayToday < self.day_of_week
		if (is_prev_week):
			return today - timedelta(days=7-(self.day_of_week-weekdayToday))
		else:
			return today + timedelta(days=(self.day_of_week - weekdayToday))

	def addMagnet(self, magnet, id):
		self.magnet = magnet
		self.torrent_id = id

	def __str__(self):
		return str(self.id) + " " + self.title

def getMyPrograms():
	cur = conn.cursor()
	sql = "select id, title, day_of_week, search_key from program_info where is_on = 1"
	cur.execute(sql)
	results = []
	for p in cur.fetchall():
		results.append(Program(p[0], p[1], p[2], p[3]))
	return results

def isAlreadyDownload(program):
	cur = conn.cursor()
	sql = "select id from download where program_id = ? and show_date = ?"
	cur.execute(sql, (program.id, program.getShowDateOnThisWeek()))
	return len(cur.fetchall()) > 0

def saveDownload(program):
	cur = conn.cursor()
	sql = "insert into download(program_id, magnet_id, show_date, download_path, file_name, delete_yn, reg_datetime) values (?, ?, ?, ?, ?, ?, datetime('now','localtime'))"
	cur.execute(sql, (program.id, program.torrent_id, program.getShowDateOnThisWeek(), "", "", "N"))
	conn.commit()

def addMagnetToTorrent(program):
	result = ""
	if isAlreadyDownload(program):
		print("already downloaded...!! = " + program.title + "("+program.getShowDateOnThisWeek()+")")
		return

	try:
		magnet = program.magnet
		result = subprocess.check_output('transmission-remote -n "anyjava:gusxo0410" -a ' + magnet, shell=True)
		if (str(result).index("success") >= 0):
			saveDownload(program)
			print("success")
			print(result)
		else:
			print("error")
			print(result)
	except subprocess.CalledProcessError:
		print("error")

	
def findMagnet(program):
	cur = conn.cursor()
	sql = "select id, magnet, title from magnet_list where title like ? AND title like ?"
	cur.execute(sql, ("%"+program.search_key+"%", "%"+program.getShowDateOnThisWeek()+"%"))
	
	results = cur.fetchall()
	for rs in results:
		program.addMagnet(rs[1].strip(), rs[0])
		print(rs[2])
		if (rs[2].find("NEXT") >= 0): break

	if len(results) > 0:
		return True
	else:
		return False
	

def main():
	print("++++++++++++++++++++++START+++++++++++++++++++++++++++")
	for p in getMyPrograms():
		if (findMagnet(p)):
			print(str(p.getShowDateOnThisWeek()) + " " + p.search_key + " " + p.magnet)
			addMagnetToTorrent(p)
		else:
			print("do not find magnet = " + p.title + "("+p.getShowDateOnThisWeek()+")")
	print("++++++++++++++++++++++++++++++++++++++++++++++++++++++")



	
main()
#addMagnetToTorrent("")

# Connection 닫기
conn.close()
