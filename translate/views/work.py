#_*_ coding: utf-8 _*_
from flask import Blueprint, render_template, redirect, url_for, flash,\
					request, jsonify
from translate.forms import UsernamePasswordForm, LoginForm
from flask.ext.login import login_user, login_required, logout_user, current_user
from translate.models import User, Over_12_anime, Trailer, User_Trailer, Characters
from translate import db
from translate import ntQueue
import json

work = Blueprint('work', __name__,
				template_folder='templates',
				static_folder='static')

@work.route('/', methods=['GET', 'POST'])
@login_required
def start():
	if request.method == 'GET':
		return render_template('work/start.html',
								current_user=current_user)
	elif request.method == 'POST':
		db_session = db.session()
		anime_data = request.get_json(force=True)[0]
		"""
		f = open("fuck.debug", "w")
		f.write(str(type(request.json)) + '\n')
		f.write(str(request.get_json(force=True)) + '\n')
		f.write(str(type(request.get_json(force=True))) + '\n')
		f.write(str(anime_json) + '\n')
		f.write(str(type(anime_json)))
		f.write(str(type(anime_json['ani_num'])))
		f.write('\n' + str(type(anime_json['ani_num'])) + str(anime_json['ani_num']))
		f.write('\n' + str(anime_json['ani_num']))
		f.close()
		return 'fuck'
		"""
		
		#return str(anime_data['title'])

		q = db_session.query(Trailer).filter(Trailer.id == int(anime_data['ani_num'])).first()

		new_anime = Over_12_anime(title=anime_data['title'],
								origin_title=anime_data.get('origin_title', ''),
								en_title=anime_data.get('en_title', ''),
								sub_title=anime_data.get('sub_title', ''),
								director=anime_data.get('director', ''),
								production=anime_data.get('production'),
								copyright=anime_data.get('copyright'),
								genres=json.dumps(anime_data.get('genres', [])),
								year=int(anime_data.get('year' , 2012)),
								ba_class=anime_data.get('ba_class', ''),
								precise=anime_data.get('precise', ''),
								epi_num=int(anime_data.get('epi_num', 0)),
								running_time=int(anime_data.get('running_time', 0)),
								nation=anime_data.get('nation', ''),
								ost=json.dumps(anime_data.get('ost', [])),
								plot=anime_data.get('plot', ''),
								intro=anime_data.get('intro', ''),
								trailer_id=int(anime_data['ani_num']))
		db_session.add(new_anime)
		db_session.commit()

		characters = anime_data['characters']
		if characters:
			for character in characters:
				new_character = Characters(character_name=character['name'],
											character_desc=character['desc'],
											#has_image=int(character['has_image']),
											anime=new_anime)
				db_session.add(new_character)
		db_session.commit()

		q.is_translate += 1
		db_session.flush()
		db_session.commit()

		# user 테이블 업데이트
		q = db_session.query(User).filter(User.id == current_user.id).first()
		q.done_cnt += 1
		db_session.flush()
		db_session.commit()

		# user_trailer 테이블에 저장
		user_trailer = User_Trailer(user_id=current_user.id, trailer_id=new_anime.trailer_id)
		db_session.add(user_trailer)
		db_session.commit()

		return jsonify({"success": "ok"})

@work.route('/rand_anime', methods=['GET'])
@login_required
def get_anime():
	anime = ntQueue.pop()

	res = {
		"ani_num": int(anime.ani_id),
		"title": anime.old_title,
		"genres": anime.genres
	}

	return jsonify(res)