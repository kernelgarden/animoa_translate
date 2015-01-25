#_*_ coding: utf-8 _*_
from wtforms.validators import Required, ValidationError

class Unique(object):
	def __init__(self, model, field, message=u'This element already exists.'):
		self.model = model
		self.field = field
		self.message = message

	def __call__(self, form, field):
		check = self.model.query.filter(self.field == field.data).first()
		if check:
			raise ValidationError(self.message)

import json
from Queue import Queue
from translate.models import Over_12_anime, Trailer

class Anime():
	"""db의 애니메이션 정보를 추상화 하여 저장하는 모델
	"""
	def __init__(self, title, genre, trailer_id):
		self.old_title = title
		self.genres = json.loads(genre)
		self.ani_id = trailer_id

class NtranslateQueue():
	"""작업을 할 목록을 큐로 만들어 쉽게 관리할 수 있게한다.
	db session을 전달받아서 db로의 전달까지 전담한다.
	"""

	def __init__(self, db_session):
		_subq = db_session.query(Trailer.id).filter(Trailer.is_translate == 0).subquery()
		self.anime_query = db_session.query(Over_12_anime).filter(Over_12_anime.trailer_id.in_(_subq)).all()
		self._tqueue = Queue(12000)

		for query in self.anime_query:
			_anime = Anime(query.old_title, query.old_genres, query.trailer_id);
			self.push(_anime) 

	def pop(self):
		if self._tqueue.qsize() == 0:
			return None
		return self._tqueue.get()

	def push(self, anime):
		self._tqueue.put(anime)