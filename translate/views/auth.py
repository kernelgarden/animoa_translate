#_*_ coding: utf-8 _*_
from flask import Blueprint, render_template, redirect, url_for, flash
from translate.forms import UsernamePasswordForm, LoginForm
from flask.ext.login import login_user, login_required, logout_user, current_user
from translate.models import User
from translate import db

auth = Blueprint('auth', __name__,
				template_folder='templates',
				static_folder='static')

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user.is_correct_password(form.password.data):
			login_user(user)
			flash('로그인 되었습니다.')

			return redirect(url_for('home.main'))
		else:
			flash('입력을 제대로 해주세요.')
			return redirect(url_for('.login'))
	#return render_template('signin.html', form=form)
	return render_template("auth/login.html", 
						form=form)

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
	form = UsernamePasswordForm()

	if form.validate_on_submit():
		user = User(username=form.username.data, password=form.password.data, name=form.name.data, done_cnt=0)
		db.session.add(user)
		db.session.commit()

		return redirect(url_for('.login'))
	return render_template('auth/signup.html', form=form)

@auth.route('/logout')
@login_required
def logout():
	logout_user()
	flash('You were logged out.')
	return redirect(url_for('home.main'))