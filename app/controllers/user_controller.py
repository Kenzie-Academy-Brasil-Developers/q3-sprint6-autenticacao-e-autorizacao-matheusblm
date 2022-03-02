from http import HTTPStatus
from flask import current_app, jsonify, request
import sqlalchemy
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models.user_model import UserModel



def sign_up():
    data = request.get_json()
    try:
        password = data.pop('password')
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
        user = UserModel.query.filter_by(email = data['email']).one()
        if user.check_password(data['password']):
            token =  create_access_token(user)
            return jsonify(access_token = token), HTTPStatus.OK
        else:
            return jsonify(error= "Usuario nao autorizado!"), HTTPStatus.UNAUTHORIZED
    except sqlalchemy.exc.NoResultFound:
        return jsonify(error= "Usuario não encontrado!"), HTTPStatus.NOT_FOUND

@jwt_required()
def get_user():
    user = get_jwt_identity()
    return jsonify(user)

@jwt_required()
def update_user():
    data = request.get_json()
    user = UserModel.query.filter_by(email=data['email']).first()
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

@jwt_required()
def delete_user():
    email = get_jwt_identity().get('email')
    user = current_app.db.session.filter_by(email=email).first()
    current_app.db.session.delete(user)
    current_app.db.session.commit()
    return jsonify(msg= f"User {user.name} has been deleted."), HTTPStatus.OK


    