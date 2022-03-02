from http import HTTPStatus
from flask import current_app, jsonify, request
import sqlalchemy
from secrets import token_urlsafe
from flask_httpauth import HTTPTokenAuth
from app.models.user_model import UserModel



auth = HTTPTokenAuth()

@auth.verify_token
def verify_token(api_key: str):
    user = UserModel.query.filter_by(api_key=api_key).first()
    return user

def sign_up():
    data = request.get_json()
    try:
        password = data.pop('password')
        data['api_key'] = token_urlsafe(16)
        user = UserModel(**data)
        user.password = password
        current_app.db.session.add(user)
        current_app.db.session.commit()
        
    except sqlalchemy.exc.IntegrityError:
        return jsonify(error= "Email ja existente!"), HTTPStatus.CONFLICT
    return jsonify(user), HTTPStatus.CREATED

def sign_in():
    data = request.get_json()
    try:
        user = UserModel.query.filter_by(email=data['email']).one()
        if user.check_password(data['password']):
            return jsonify(api_key= user.api_key), HTTPStatus.OK
    except sqlalchemy.exc.NoResultFound:
        return jsonify(error= "Usuario não encontrado!"), HTTPStatus.NOT_FOUND

@auth.login_required
def get_user():
    user = auth.current_user()
    return jsonify(user)

@auth.login_required
def update_user():
    data = request.get_json()
    user = auth.current_user()
    if data.get('email'):
        data.pop('email')
    if data.get('password'):
        password = data.pop('password')
        user.password = password
    for key, value in data.items():
        setattr(user, key, value)
    current_app.db.session.add(user)
    current_app.db.session.commit()
    return jsonify(user), HTTPStatus.OK

@auth.login_required
def delete_user():
    user = auth.current_user()
    current_app.db.session.delete(user)
    current_app.db.session.commit()
    return jsonify(msg= f"User {user.name} has been deleted."), HTTPStatus.OK