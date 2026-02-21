from datetime import datetime
import secrets

from flask import session

from flask_anime_api.model.schemas import UserAuthSchema, UserDTO
from flask_anime_api.model.database import db
from flask_anime_api.user.repository import UserRepository

class AuthService:
    __user_repo = UserRepository(db)

    @classmethod
    def login(cls, creds: UserAuthSchema) -> UserDTO:
        u = cls.__user_repo.authenticate(creds)
        if u:
            user_data = {
                'user_id': u.id,
                'username': u.username,
                'is_admin': u.is_admin,
                'session_id': secrets.token_urlsafe(32)
            }

            session['user'] = user_data
            session.modified = True

            return u

        return None
    
    @classmethod
    def get_current_user(cls):
        return session.get('user')

    @classmethod
    def is_authenticated(cls):
        return 'user' in session

    @classmethod
    def logout(cls):
        session.pop('user', None)
        session.clear()
