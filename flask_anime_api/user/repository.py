from sqlalchemy.orm import Session
from sqlalchemy import select

from flask_anime_api.model.user import User
from flask_anime_api.model.database import Database
from flask_anime_api.model.schemas import UserCreateSchema, UserDTO

class UserRepository():
    def __init__(self, db: Database):
        self.db = db

    def get_by_id(self):
        ...

    def get_all(self) -> list[UserDTO]:
        with self.db.session_scope() as s:
            users = s.scalars(select(User)).all()
            data = [UserDTO(**u.to_dict()) for u in users]
            return data

    def update(self):
        ...

    def __user_existed(self, session: Session, email: str = None) -> bool:
        u = session.scalars(select(User).filter_by(email=email)).first()
        if u:
            return True
        return False

    def create(self, user_data: UserCreateSchema) -> UserDTO:
        with self.db.session_scope() as s:
            if self.__user_existed(s, email=user_data.email):
                return ValueError('email existed')

            u = User(username=user_data.username, email=user_data.email, is_admin=user_data.is_admin)
            u.set_password(user_data.password)
            s.add(u)
            s.flush()
            return UserDTO(**u.to_dict())
            

    def delete(self):
        ...