#_*_ coding: utf-8 _*_
import sys
import re
import pickle
import json
from translate import db
from translate.models import *

if __name__ == '__main__':
	data = pickle.load(open("save_dict.p", "rb"))
	date_list = pickle.load(open("date_list.p", "rb"))

	new_anime_list = []

	for (num, metadata) in data.items():
		flag = False
		years = metadata.get('dates', [])
		for year in years:
			m = re.findall(r"(\d{4})", year)
			for i in m:
				if '2012' <= i:
					flag = True
		if flag == True:
			trailer = Trailer(id=int(num), is_translate=0)
			db.session.add(trailer)
			db.session.commit()

			ani_name = metadata['ani_name'] + '(' + metadata['precision'] + ')'
			genres = json.dumps(metadata.get('genres', []))
			anime = Over_12_anime(old_title=ani_name, old_genres=genres,
									translate_type=0, anime=trailer)
			db.session.add(anime)
			db.session.commit()
			print "done {0}".format(ani_name)
			#new_anime_list.append(tuple((num, metadata['ani_name'], metadata['precision'])))
			#print num
	print "2012년 이후작 추출 완료"
	
	#print new_anime_list
	#print len(new_anime_list)

	#	years = re.findall(r"(\d{4})", metadata['dates'])
	"""
	for date in date_list:	# 전체 리스트에서 작품 하나를 뽑는다
		for data in date:	# 작품 하나에서 날짜 데이터를 받음
			flag = False
			years = re.findall(r"(\d{4})", data)	
			for year in years:
				if '2012' <= year:
					flag = True
		print '\n'
	"""