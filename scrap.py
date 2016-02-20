from urllib.request import urlopen
from bs4 import BeautifulSoup
import sqlite3
import ssl
import urllib

TORRENT_HOST = "https://torrentwal.com/"

# SQLite DB 연결
conn = sqlite3.connect("test.db")

def soupOf(url):
	context = ssl._create_unverified_context()
	req = urllib.request.Request(TORRENT_HOST + url, headers={'User-Agent': 'Wget/1.18 (darwin16.0.0)'})
	html = urlopen(req, context=context)
	return BeautifulSoup(html.read(), "html.parser")

def loadTorrentContentUrl(program_type, detailUrl):
#	bsObj = soupOf("board.php?mode=list&b_id=tent")
	bsObj = soupOf(detailUrl)
	links = bsObj.findAll("td", {"class": "subject"})
	programs = []
	maxWrid = getLastestWrId(program_type)
	print("maxWrid: " + str(maxWrid))
	for aTag in links:
		print(getUrl(aTag))
		print(getTitle(aTag))
		title = getTitle(aTag).strip()
		url = getUrl(aTag)
#		url = loadTorrentContent(getUrl(aTag)).strip()
#		print("load url>> " + url);
#		wrid = url.split("?")[1].split("&")[1].split("=")[1];
		wrid = url[3:].split("/")[1][:-5]
		if maxWrid >= int(wrid):
			print("SKIP!! => " + wrid + "is lastest Wrid.")
			break;
		if title.find("720") >= 0:
			magnet = getMargnet(url)
			if (magnet != ""):
				program = [[wrid, title, getMargnet(url), program_type]]
				programs += program
	if len(programs) > 0:
		savePrograms(programs)
	else:
		print('no element for insert.')

def getUrl(aTag):
	return aTag.findAll("a")[0]["href"][3:]

def getTitle(aTag):
	return aTag.findAll("a")[0].get_text()

def loadTorrentContent(url):
	return soupOf(url).find(id="external-frame")["src"]
	
def getMargnet(url):
	magnets = soupOf(url).find(text="MagNet:").parent.findNext('a').get_text()
	if (len(magnets) > 0):
#		return soupOf(url).findAll("div", {"class": "torrent_magnet"})[0].a.get_text()
		return magnets
	else:
		return ""

def getLastestWrId(program_type):
	cur = conn.cursor()
	sql = "select ifnull(max(wrid), 0) from magnet_list where program_type = '"+program_type+"'"
	cur.execute(sql)
	rs = cur.fetchall()
	return rs[0][0]

def savePrograms(lists):
	cur = conn.cursor()
	sql = "insert into magnet_list(wrid, title, magnet, program_type) values (?, ?, ?, ?)"
	cur.executemany(sql, lists)
	conn.commit()

# 예능
print("STARTING ent")
loadTorrentContentUrl("ENT", "torrent_variety/torrent1.htm")
# 드라마
print("STARTING drama")
loadTorrentContentUrl("DRAMA", "torrent_tv/torrent1.htm")
# 시사
#print("STARTING tv")
#loadTorrentContentUrl("TV", "board.php?mode=list&b_id=tv")
print("END")

# Connection 닫기
conn.close()
