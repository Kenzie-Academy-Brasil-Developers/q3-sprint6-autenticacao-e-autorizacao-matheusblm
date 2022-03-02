from flask import Flask
from flask_jwt_extended import JWTManager
from environs import Env

env = Env()

def init_app(app: Flask):
    app.config["JWT_SECRET_KEY"] = env('JWT_SECRET_KEY')
    JWTManager(app)