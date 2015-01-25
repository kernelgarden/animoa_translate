from sqlalchemy.ext.hybrid import hybrid_property
from flask.ext.login import UserMixin
from . import login_manager
from . import bcrypt, db

@login_manager.user_loader
def get_user(ident):
	return User.query.get(int(ident))

class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(64), unique=True)
	_password = db.Column(db.String(128))
	name = db.Column(db.String(20))
	done_cnt = db.Column(db.Integer)
	done_list = db.relationship('User_Trailer', backref='author', lazy='dynamic')

	@hybrid_property
	def password(self):
		return self._password

	@password.setter
	def _set_password(self, plaintext):
		self._password = bcrypt.generate_password_hash(plaintext)

	def is_correct_password(self, plaintext):
		return bcrypt.check_password_hash(self._password, plaintext)

	def __repr__(self):
		return '<User %r>' % (self.username)


class User_Trailer(db.Model):
	__tablename__ = 'user_trailer'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
	trailer_id = db.Column(db.Integer, db.ForeignKey('trailer.id'))

	def __repr__(self):
		return '<User-anime %r-%r>' % (self.user_id, self.trailer_id)


class Trailer(db.Model):
	__tablename__ = 'trailer'
	id = db.Column(db.Integer, primary_key=True, autoincrement=False, unique=True)
	is_translate = db.Column(db.Integer)
	info = db.relationship('User_Trailer', backref='anime', lazy='dynamic')
	anime_info = db.relationship('Over_12_anime', backref='anime', lazy='dynamic')

	def __repr__(self):
		return '<id %r>' % (self.id)


class Over_12_anime(db.Model):
	__tablename__ = 'anime_info'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	old_title = db.Column(db.String(200))
	old_genres = db.Column(db.String(300))
	title = db.Column(db.String(200))
	origin_title = db.Column(db.String(200))
	en_title = db.Column(db.String(200))
	sub_title = db.Column(db.String(300))
	director = db.Column(db.String(200))
	production = db.Column(db.String(300))
	copyright = db.Column(db.String(200))
	genres = db.Column(db.String(300))
	year = db.Column(db.Integer)
	ba_class = db.Column(db.String(40))
	precise = db.Column(db.String(40))
	epi_num = db.Column(db.Integer)
	running_time = db.Column(db.Integer)
	nation = db.Column(db.String(30))
	ost = db.Column(db.String(500))
	plot = db.Column(db.String(5000))
	intro = db.Column(db.String(5000))
	trailer_id = db.Column(db.Integer, db.ForeignKey('trailer.id'))
	translate_type = db.Column(db.Integer)
	characters = db.relationship('Characters', backref='anime', lazy='dynamic')

	def __repr__(self):
		return '<Anime %r>' % (self.title)


class Characters(db.Model):
	__tablename__ = 'characters'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	anime_id = db.Column(db.Integer, db.ForeignKey('anime_info.id'))
	character_name = db.Column(db.String(70))
	character_desc = db.Column(db.String(3000))
	has_image = db.Column(db.Integer)
	voices = db.relationship('Voices', backref='character', lazy='dynamic')

	def __repr__(self):
		return '<Character %r>' % (self.character_name)


class Voices(db.Model):
	__tablename__ = 'voices'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	characters_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
	voice_name = db.Column(db.String(100))
	nation_type = db.Column(db.String(30))

	def __repr__(self):
		return '<Voice %r>' % (self.voice_name)