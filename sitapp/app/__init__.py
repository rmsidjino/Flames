from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment

from config import config

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_view = 'itemRegister.login'
import pymongo
conn = pymongo.MongoClient('mongodb://db:27017')
db = conn.get_database('flames')

from gridfs import GridFS
from gridfs.errors import NoFile

fs = GridFS(db)

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()

def create_app(config_name):
	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object(config[config_name])
	app.config.from_pyfile('config.py') 
	
	config[config_name].init_app(app)
	bootstrap.init_app(app)
	moment.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)

    # attach routs and custom error pages here

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)
	from .auth import auth as auth_blueprint
	app.register_blueprint(auth_blueprint, url_prefix="/auth")
	from .mypage import mypage as mypage_blueprint
	app.register_blueprint(mypage_blueprint, url_prefix="/mypage")
	from .itemRegister import itemRegister as itemRegister_blueprint
	app.register_blueprint(itemRegister_blueprint, url_prefix="/itemRegister")	


	return app
