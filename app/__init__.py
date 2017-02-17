from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_oauthlib.provider import OAuth2Provider
from .confs import Core

db = SQLAlchemy()
oauth = OAuth2Provider()
def create_app():
	print("Creating App")
	app = Flask( __name__)
	app.config.from_object(Core)
	db.init_app(app)
	oauth.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	from .api import api as api_blueprint
	app.register_blueprint(api_blueprint)

	return app