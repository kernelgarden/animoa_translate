#_*_ coding: utf-8 _*_
import re
import sys
import os
import urllib
import pickle
import json
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding("utf-8")

class BestAnimation():
	"""BestAnimation
	"""
	def __init__(self):
		pass

class SearchPage():
	"""bestAnimation의 게시물 페이지(sorted by 등급별)
	1: BA-7, 2: BA-13, 3: BA-17, 4: BA-R, 5: BA-X
	"""
	anime = []	# 애니메이션 번호들
	pages = {}	# page 정보들이 담김
	def_url = 'http://www.bestanimation.co.kr'
	search_url = 'http://www.bestanimation.co.kr/Library/Animation/Search.php?mainType=6&mainKeyword='
	search_type = {'BA-7': '1', 'BA-13': '2', 'BA-17': '3', 'BA-R': '4', 'BA-X': '5'}

	def __init__(self, s_type):
		self.search_url = self.search_url + self.search_type[s_type]
		self.buildPage()
		for page_num in range(1, self.page_len+1):
			self.parsePage(page_num)

	# 검색 창의 page의 끝까지 긁어와서 soup객체로 만들어 저장
	def buildPage(self):
		query = '&subType=&subKeyword=&page='
		url = self.search_url + query
		i = 1

		while (True):
			u = urllib.urlopen(url+str(i))
			stream = u.read()
			u.close()
			#self.pages[i] = {}
			self.pages[i] = BeautifulSoup(stream, "lxml")
			print i
			a_list = self.pages[i].find_all('td', attrs={'height': 20})[1].find_all('a')
			if (url+str(i) == self.def_url + a_list[len(a_list)-1]['href']): # 현재 페이지가 마지막인지 검사
				break
			i += 1
		self.page_len = i

	# 현재 페이지를 파싱한다
	def parsePage(self, page_num):
		ani_list = self.pages[page_num].find_all('td', attrs={'width': 710, 'height': 35})
		for anime in ani_list:
			ani_url = self.def_url + anime.a['href']
			res = re.search(r"Idx=(\d*)&", ani_url)
			self.anime.append(int(res.group(1)))


class AnimePage():
	"""애니메이션의 세부 페이지에 대한 객체
	"""
	_info_url = 'http://www.bestanimation.co.kr/Library/Animation/Info.php?Idx='
	_character_url = 'http://www.bestanimation.co.kr/Library/Animation/Character.php?Idx='
	_synopsis_url = 'http://www.bestanimation.co.kr/Library/Animation/Synopsis.php?Idx='

	def __init__(self, ani_num):
		self._current_ani_num = int(ani_num)
		self.downHtml(self._current_ani_num)
		if not os.path.exists("img"):
			os.makedirs("img")	
		self.parseAll()

	def openUrl(self, url):
		u = urllib.urlopen(url)
		stream = u.read()
		u.close()
		return stream

	# 애니의 번호를 받아 beautifulsoup 포맷으로 변환시켜 저장
	def downHtml(self, ani_num):
		# info html 다운
		self._info_html = BeautifulSoup(self.openUrl(self._info_url + str(ani_num)))

		# character html 다운
		self._character_url = BeautifulSoup(self.openUrl(self._character_url + str(ani_num)))

		# synopsis html 다운
		self._synopsis_url = BeautifulSoup(self.openUrl(self._synopsis_url + str(ani_num)))

	# 애니의 기본적인 정보들을 파싱해온다
	def getInfo(self):
		"""self._anime = {'id': int, 'title': unicode, 'origin_title': unicode,
			'en_title': unicode, 'sub_titles': list, 'director': unicode,
			'productions': list, 'copyright': list, 'desc': unicode
			'genres': list, 'year': int, 'BA_class': unicode, 'precise': string, 
			'epi_num': int, 'running_time': int(minutes), 'nation': unicode
		}
		"""
		cnt = 0
		skip_list = [6, 9]	# 각본, 음악 생략

		self._anime = {'id': self._current_ani_num}
		info_list = self._info_html.find_all('table', attrs={'width': 610})[0].\
						find_all('tr', attrs={'height': 24})

		# 제목 
		self._anime['title'] = info_list[0].find_all('td')[1].text.strip()
		# 원제
		self._anime['origin_title'] = info_list[1].find_all('td')[1].text.strip()
		# 영제
		self._anime['en_title'] = info_list[2].find_all('td')[1].text.strip()
		# 부제
		self._anime['sub_titles'] = []
		sub_titles = info_list[3].find_all('td')[1].text.split('|')
		for title in sub_titles:
			self._anime['sub_titles'].append(title.strip())
		# 감독
		self._anime['director'] = info_list[4].find_all('td')[1].text.strip()
		# 제작
		self._anime['productions'] = []
		productions = info_list[7].find_all('td')[1].text.split('|')
		for production in productions:
			self._anime['productions'].append(production.strip())
		# 저작권
		self._anime['copyright'] = info_list[8].find_all('td')[1].text.strip()
		# 장르
		self._anime['genres'] = []
		genres = info_list[10].find_all('td')[1].text.split('|')
		for genre in genres:
			self._anime['genres'].append(genre.strip())
		# 제작년도
		self._anime['year'] = int(info_list[11].find_all('td')[1].text.strip())
		# BA등급
		self._anime['BA_class'] = info_list[12].find_all('td')[1].text.strip()
		# 구분
		self._anime['precise'] = info_list[13].find_all('td')[1].text.strip()
		# 총화수 & 상영시간
		episode = info_list[14].find_all('td')[1].text.strip()
		epi_info = [info.strip() for info in episode.split('X')]
		if (len(epi_info) == 2):
			running_time = re.match(r"(\d*)\.*", epi_info[0])
			self._anime['running_time'] = int(running_time.groups()[0])
			epi_num = re.match(r"(\d*)\.*", epi_info[1])
			self._anime['epi_num'] = int(epi_num.groups()[0])
		else:
			self._anime['running_time'] = 0
			self._anime['epi_num'] = 0
		# 제작국
		self._anime['nation'] = info_list[15].find_all('td')[1].text.strip()

		# 애니 사진 저장
		img_dir = 'img/' + str(self._current_ani_num)
		img_url = 'http://data.bestanimation.co.kr/HNY_img/ani_image/%d/BESTANIME+tim001.jpg'\
						% self._current_ani_num
		if not os.path.exists(img_dir):
			os.makedirs(img_dir)
		u = urllib.urlopen(img_url)
		stream = u.read()
		u.close()
		img_file = open(img_dir+"/"+str(self._current_ani_num)+".jpg", "wb")
		img_file.write(stream)
		img_file.close()

		# 작품 소개
		self._anime['desc'] = self._info_html.find_all('table', attrs={'width': 820})[0].td.text.strip()

	# 애니에 나오는 캐릭터들의 정보를 파싱해온다
	def getCharacter(self):
		"""self._characters = {'name of character': {
			'voices': list, 'desc': string	
		}}
		"""
		characters_dir = "img/" + str(self._current_ani_num) + "/characters" 
		if not os.path.exists(characters_dir):
			os.makedirs(characters_dir)
		self._characters = {}
		character_list = self._character_url.find_all('table', attrs={'width': 820})[0].\
							find_all('tr', attrs={'height': 30})

		if (len(character_list) == 0):	# 캐릭터 정보들이 없는 경우
			return None
		del(character_list[0]) 	# 첫번쨰 tr은 무의미한 데이터
		for character in character_list:
			# 이름 파싱
			c_name = character.b.text.replace('\t', '').replace('\r\n', '')
			self._characters.setdefault(c_name, {})

			# 캐릭터 사진 파싱
			c_img = character.td.img['src']
			if c_img == '/Resource/Images/blankbox/no_character_img.gif':
				self._characters[c_name]['has_image'] = 0
				c_img = 'http://www.bestanimation.co.kr/Resource/Images/blankbox/no_character_img.gif'
			else:
				self._characters[c_name]['has_image'] = 1
			u = urllib.urlopen(c_img)
			stream = u.read()
			u.close()
			# 사진 저장
			buf = c_name.replace('/', ',')
			file_name = os.path.join(characters_dir, buf+".jpg")
			img_file = open(file_name, "wb")
			img_file.write(stream)
			img_file.close()

			# 성우진 파싱
			c_voice_list = character.find_all('a')
			if (len(c_voice_list) == 0): continue		# 성우정보가 없는 경우
			self._characters[c_name].setdefault('voices', [])
			for voice in c_voice_list:
				if voice.u != None:
					self._characters[c_name]['voices'].append(voice.u.text.strip())

			# 캐릭터 정보 파싱 -수정 요망
			c_desc = re.search(r"<br>\s*<br>\s*([\s\S]*)<\/br>", character.prettify())	
			if (c_desc == None): continue		# 캐릭터 정보가 없는 경우
			self._characters[c_name]['desc'] = c_desc.group(1).replace("<br>", "").\
					replace("</br>", "").strip()

	def getSynopsis(self):
		"""self._synopsis = unicode
		"""
		synopsis = self._synopsis_url.find_all('table', attrs={'width': 820})[0]
		self._synopsis = synopsis.text.strip()
		if self._synopsis == "데이터가 없습니다.":
			self._synopsis = ''

	def parseAll(self):
		# 애니메이션 페이지를 파싱한다
		self.getInfo()
		self.getSynopsis()
		self.getCharacter()

		self._anime['synopsis'] = self._synopsis
		self._anime['characters'] = self._characters

	def getParseData(self):
		return self._anime

if __name__ == '__main__':
	page_BA7 = SearchPage('BA-7')
	print "BA-7 완료"
	#page_BA13 = SearchPage('BA-13')
	#print "BA-13 완료"
	#page_BA17 = SearchPage('BA-17')
	#print "BA-17 완료"
	print "-"*60

	f = open("ba7_parse.txt", "w")
	ba7_list = page_BA7.anime
	for ani_num in ba7_list:
		anime = AnimePage(ani_num)
		anime = json.dumps(anime.getParseData())
		f.write(anime + '\n')
	f.close()
	#anime = AnimePage(ba7_list[0])
	"""
	anime = AnimePage(1429)
	print anime.getParseData()
	"""


"""
	pickle.dump(page_BA7, open("ba7.p", "wb"))
	pickle.dump(page_BA13, open("ba13.p", "wb"))
	pickle.dump(page_BA17, open("ba17.p", "wb"))
"""
