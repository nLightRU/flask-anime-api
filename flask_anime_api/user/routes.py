from flask import Blueprint

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


@users_bp.put('/<user_id>/')
def update_user():
    ...


@users_bp.delete('/<user_id>/')
def delete_user():
    ...