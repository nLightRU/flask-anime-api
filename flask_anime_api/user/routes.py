from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from flask_anime_api.user.service import UserService
from flask_anime_api.model.schemas import UserCreateSchema

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.get('/<user_id>/profile')
def get_user_profile():
    ...


@users_bp.get('/<user_id>')
def get_user():
    ...


@users_bp.get('/')
def get_users():
    ...

@users_bp.post('')
def create_user():
    try:
        data = request.get_json()
        user_data = UserCreateSchema(**data)
    except ValidationError:
        raise
        return f'Wrong input', 400
    
    s = UserService()

    try:
        u = s.create(user_data)
    except:
        raise
    
    return jsonify(**u.model_dump())


@users_bp.put('/<user_id>/')
def update_user():
    ...


@users_bp.delete('/<user_id>/')
def delete_user():
    ...