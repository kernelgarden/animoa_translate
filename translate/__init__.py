import sys
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.bcrypt import Bcrypt

reload(sys)
sys.setdefaultencoding("utf-8")

app = Flask(__name__)
app.config.from_object('config')


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

from .models import User
from .utils import NtranslateQueue
ntQueue = NtranslateQueue(db.session())

from .views.home import home
from .views.auth import auth
from .views.work import work

app.register_blueprint(home)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(work, url_prefix='/work')

@login_manager.user_loader
def load_user(userid):
	return User.query.filter(User.id==int(userid)).first()