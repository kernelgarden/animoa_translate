#_*_ coding: utf-8 _*_
from flask import Blueprint, render_template, url_for, jsonify, request, abort, send_file 
from flask.ext.login import login_user, login_required, logout_user, current_user

from translate import db, app
from translate.models import Over_12_anime, Characters

from math import ceil
import json

api = Blueprint('api', __name__)

@api.route('/anime/get_anime', methods=["GET"])
@login_required
def ret_anime_chunk():
	# 장르 룩업 테이블
	genre_lookup = {0: u'ALL', 1: u'3D 애니', 2: u'SF', 4: u'구조물', 8: u'갱스터', 16: u'다큐멘터리', \
					32: u'단편', 64: u'드라마', 128: u'레이싱', 256: u'로맨스', 512: u'로봇', 1024: u'마법',\
					2048: u'메이드', 4096: u'메카닉', 8192: u'뮤지컬', 16384: u'미스테리',\
					32768: u'범죄물', 65536: u'서부영화', 131072: u'성인물', 262144: u'스릴러',\
					524288: u'스포츠', 1048576: u'시대물', 2097152: u'아동물', 4194304: u'액션',\
					8388608: u'어드벤쳐', 16777216: u'위인전', 33554432: u'전쟁물',\
					67108864: u'코메디', 134217728: u'클레이메이션', 268435456: u'학원물',\
					536870912: u'호러물', 1073741824: u'판타지', 2147483648: u'변신',\
					4294967296: u'BL', 8589934592: u'일상'}

	# request 처리
	chunk_num = request.args.get('chunk_num', -1, type=int)	# 요청한 chunk 번호
	count = request.args.get('count', -1, type=int) # 요청한 정보 갯수
	genre = request.args.get('genre', -1, type=int) # 요청한 장르

	if genre == -1 or genre >= 17179869184:
		return abort(400)
	if count == -1:
		return abort(400)
	if chunk_num == -1:
		return abort(400)

	ses = db.session()
	# 장르 필터링
	if genre == 0:
		#total_data = ses.query(Over_12_anime).filter(Over_12_anime.id >= 1194).count()
		q = ses.query(Over_12_anime).filter(Over_12_anime.id >= 1194).all()
		total_data = len(q)
	else:
		query_string = "select * from anime_info where"
		query = []
		genre_list = [genre_lookup[key] for (key, val) in genre_lookup.items() if genre & key]
		for genre in genre_list:
			genre = unicode(genre.replace(' ', '%'))
			query.append(unicode(' genres like "%{0}%"'.format(genre)))
		query_string += ' or '.join(query)
		q = ses.query(Over_12_anime).from_statement(query_string+" group by trailer_id").all()
		#return (q[0].title + q[0].genres)
		total_data = len(q)
		return str(len(q))

	# 연산에 필요한 정보 계산
	start_idx = (chunk_num - 1) * count
	end_idx = (chunk_num * count) - 1
	num_of_chunk = int(ceil(total_data/count))

	if num_of_chunk < chunk_num:
		return abort(405)

	# 장르 필터링

	res = 	\
	{"meta": {
		"chunk_num": chunk_num,
		"remain_count": num_of_chunk - chunk_num,
		"count": count,
		"genre": genre
		},
		"data": {}
	}	
	#q = ses.query(Over_12_anime).filter(Over_12_anime.id >= 1194).all()

	res['data'] = []
	for idx in range(start_idx, end_idx + 1):
		anime = q[idx]
		temp = {}
		temp['origin_id'] = anime.trailer_id
		temp['title'] = anime.title
		temp['origin_title'] = anime.origin_title
		temp['en_title'] = anime.en_title
		temp['sub_title'] = anime.sub_title
		temp['director'] = anime.director
		temp['production'] = anime.production
		temp['copyright'] = anime.copyright
		temp['genres'] = []
		for genre in json.loads(anime.genres):
			temp['genres'].append(genre.encode('utf-8'))
			#temp['genres'] = anime.genres
		temp['year'] = int(anime.year)
		temp['ba_class'] = anime.ba_class
		temp['precise'] = anime.precise
		temp['epi_num'] = int(anime.epi_num)
		temp['running_time'] = int(anime.running_time)
		temp['nation'] = anime.nation
		temp['plot'] = anime.plot
		temp['intro'] = anime.intro
		temp['characters'] = {}

		for c in anime.characters:
			temp['characters'][c.character_name] = c.character_desc

		res['data'].append(temp)

	return jsonify(res)