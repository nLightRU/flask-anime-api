from uuid import UUID

from flask import Blueprint, request, jsonify
from pydantic import ValidationError

from flask_anime_api.user.service import UserService
from flask_anime_api.model.schemas import UserDTO, UserCreateSchema, UserUpdateSchema

users_bp = Blueprint('users', __name__, url_prefix='/api/users')


@users_bp.get('/<user_id>/profile')
def get_user_profile():
    ...


@users_bp.get('/<user_id>')
def get_user():
    ...


@users_bp.get('/')
def get_users():
    s = UserService()
    try:
        users = s.get_all()
    except:
        raise

    return jsonify([u.model_dump() for u in users])

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
def update_user(user_id):
    try:
        json = request.get_json()
        user_data = UserUpdateSchema(**json)
    except ValidationError:
        return f'Validation error for user {user_id}', 400
    
    s = UserService()
    try:
        u = s.update(user_id=UUID(user_id), user_data=user_data)
    except ValueError:
        return f'No user with id {user_id}', 404

    return jsonify(**u.model_dump())


@users_bp.delete('/<user_id>/')
def delete_user(user_id):
    ...