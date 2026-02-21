from flask import Blueprint, request
from werkzeug.exceptions import Unauthorized
from pydantic import ValidationError

from flask_anime_api.model.schemas import UserAuthSchema
from flask_anime_api.auth.service import AuthService
from flask_anime_api.auth.middleware import login_required

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.post('/login/')
def login():
    try:
        json = request.get_json()
        creds = UserAuthSchema(**json)
    except ValidationError:
        return Unauthorized('Wrong email or password')
    
    try:
        user_data = AuthService.login(creds)
        if user_data:
            return f'Access granted', 200
        else:
            return Unauthorized('Wrong email or password')
    except:
        raise
   

@auth_bp.post('/logout/')
@login_required
def logout():
    try:
        AuthService.logout()
    except:
        raise
    return 'OK', 200