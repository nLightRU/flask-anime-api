from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from flask_anime_api.model.user import User
from flask_anime_api.model.database import Database
from flask_anime_api.model.schemas import BaseUser, UserDTO, UserCreateSchema, UserUpdateSchema

class UserRepository():
    def __init__(self, db: Database):
        self.db = db

    def __user_existed(self, session: Session, email: str = None, user_id: UUID = None) -> bool:
        if email:
            u = session.scalars(select(User).filter_by(email=email)).first()
        elif user_id:
            u = session.get(User, user_id)
        if u:
            return True
        return False

    def get_by_id(self):
        ...

    def get_all(self) -> list[UserDTO]:
        with self.db.session_scope() as s:
            users = s.scalars(select(User)).all()
            data = [UserDTO(**u.to_dict()) for u in users]
            return data

    def update(self, user_id: UUID, user_data: UserUpdateSchema) -> UserDTO:
        with self.db.session_scope() as s:
            if not self.__user_existed(s, user_id=user_id):
                raise ValueError('Not user with such id')
            
            u = s.get(User, user_id)
            for k , v in user_data.model_dump().items():
                if hasattr(u, k) and getattr(u, k) != v:
                    setattr(u, k, v)
            
            s.flush()
            s.refresh(u)
            return UserDTO(**u.to_dict())



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