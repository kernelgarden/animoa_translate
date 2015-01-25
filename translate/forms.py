#_*_ coding: utf-8 _*_
from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required

from .utils import Unique
from translate.models import User

class UsernamePasswordForm(Form):
	username = TextField('Username', validators=[Required(),
							Unique(
								User,
								User.username,
								message='There is aleready an account with that username.')])
	password = PasswordField('Password', validators=[Required()])	
	name = TextField('이름', validators=[Required()])

class LoginForm(Form):
	username = TextField('Username', validators=[Required()])
	password = PasswordField('Password', validators=[Required()])