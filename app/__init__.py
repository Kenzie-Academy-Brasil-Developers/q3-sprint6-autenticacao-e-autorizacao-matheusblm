from flask import Flask
from app.configs import database, migration, jwt
from app import routes
from environs import Env

env = Env()

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = env("SQLALCHEMY_DATABASE_URI")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = False

    database.init_app(app)
    migration.init_app(app)
    jwt.init_app(app)
    routes.init_app(app)

    return app