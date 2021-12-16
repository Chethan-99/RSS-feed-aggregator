from flask import Flask, app

from url_shortener.api import initialize_routes
from .models import db
from .routes import views
from flask_restful import Api

def create_app(config_file='settings.py'):
    app = Flask(__name__)
    api =   Api(app)
    app.config.from_pyfile(config_file)
    app.secret_key = 'development'

    db.init_app(app)

    app.register_blueprint(views)

    initialize_routes(api)

    return app