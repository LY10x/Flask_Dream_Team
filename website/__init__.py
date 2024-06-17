from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'skibidi smeg'
    app.config['SQLALCHEMY'] = f'sqlit:///{DB_NAME}'

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app