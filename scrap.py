from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3

TORRENT_HOST = "http://www.tfreeca22.com/"
# SQLite DB 연결
conn = sqlite3.connect("test.db")

def soupOf(url):
	html = urlopen(TORRENT_HOST + url)
	return BeautifulSoup(html.read(), "html.parser")

def loadTorrentContentUrl():
	bsObj = soupOf("board.php?mode=list&b_id=tent")
	links = bsObj.findAll("td", {"class": "subject"})
	programs = []
	maxWrid = getLastestWrId()
	for aTag in links:
		print(getUrl(aTag))
		print(getTitle(aTag))
		title = getTitle(aTag).strip()
		url = loadTorrentContent(getUrl(aTag)).strip()
		wrid = url.split("?")[1].split("&")[1].split("=")[1];
		if maxWrid < int(wrid):
			print("SKIP!! => " + wrid + "is lastest Wrid.")
			break;
		if title.find("720") >= 0:
			program = [[wrid, title, getMargnet(url)]]
			programs += program
	if len(programs) > 0:
		savePrograms(programs)
	else:
		print('no element for insert.')

def getUrl(aTag):
	return aTag.findAll("a")[1]["href"]

def getTitle(aTag):
	return aTag.findAll("a")[1].get_text()

def loadTorrentContent(url):
	return soupOf(url).find(id="external-frame")["src"]
	
def getMargnet(url):
	return soupOf(url).findAll("div", {"class": "torrent_magnet"})[0].a.get_text()

def getLastestWrId():
	cur = conn.cursor()
	sql = "select max(wrid) from magnet_list"
	cur.execute(sql)
	return cur.fetchall()[0][0]

def savePrograms(lists):
	cur = conn.cursor()
	sql = "insert into magnet_list(wrid, title, magnet) values (?, ?, ?)"
	cur.executemany(sql, lists)
	conn.commit()

loadTorrentContentUrl();

# Connection 닫기
conn.close()
