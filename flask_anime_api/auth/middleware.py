from functools import wraps
from typing import Callable

from flask import session
from werkzeug.exceptions import Unauthorized, Forbidden

from flask_anime_api.auth.service import AuthService

def login_required(view_fn: Callable) -> Callable:
    @wraps(view_fn)
    def decorated(*args, **kwargs):
        if not AuthService.is_authenticated():
            return Unauthorized('You need to login')
        
        return view_fn(*args, **kwargs)
    
    return decorated


def admin_required(view_fn: Callable) -> Callable:
    @wraps(view_fn)
    def decorated(*args, **kwargs):
        if 'user' not in session:
            return Unauthorized('You need to login')
        
        user_data = AuthService.get_current_user()
        if not user_data or not user_data.get('is_admin'):
            return Forbidden('You are not admin')

        return view_fn(*args, **kwargs)
    
    return decorated