#_*_ coding: utf-8 _*_
from flask import Blueprint, render_template, url_for, jsonify, request, abort, send_file
from flask.ext.login import login_user, login_required, logout_user, current_user
from translate.models import User
from translate import db, app
from translate.models import Over_12_anime

import os

home = Blueprint('home', __name__,
				template_folder='templates',
				static_folder='static',
				static_url_path='/static/home',
				url_prefix='/')

ALLOWED_EXTENSIONS = ['jpg', 'jpeg']

@home.route('/')
def main():
	return render_template('home/index.html',
							current_user=current_user)

@home.route('image', methods=['GET', 'POST'])
@login_required
def drive_image():
	if request.method == 'GET':
		ani_num = request.args.get('ani_num', 0, type=int)
		if ani_num == 0:
			abort(400)

		file_name = "static/img/" + str(ani_num) + "/" + str(ani_num) + ".jpg"
		if not os.path.isfile(os.path.join(app.root_path, file_name)):
			return send_file("static/img/ene_love.gif", mimetype='image/gif')
		return send_file(file_name, mimetype='image/jpg')
	elif request.method == 'POST':
		# 0: 애니메이션, 1: 캐릭터
		file_type = int(request.form['type'])
		ani_num = int(request.form['ani_num'])
		default_path = os.path.join(app.root_path, "static/img/", str(ani_num))

		if not os.path.exists(default_path):
				os.makedirs(default_path)

		if file_type == 0:
			file = request.files['file']
			if file and allowed_file(file.filename):
				filename = os.path.join(default_path, file.filename)
				file.save(filename)
				return jsonify({"success": True})
			return jsonify({"success": True})

		elif file_type == 1:
			chracter_name = request.form['character_name']
			character_dir = default_path + "/characters"

			if not os.path.exists(character_dri):
				os.makedirs(character_dir)
			file = request.files['file']
			if file and allowed_file(file.filename):
				filename = os.path.join(character_dir, file.filename)
				file.save(filename)
				return jsonify({"success": True})
			return jsonify({"success": False})

		else: abort(400)

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].strip() in ALLOWED_EXTENSIONS