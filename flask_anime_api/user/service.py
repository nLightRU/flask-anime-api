from uuid import UUID

from flask_anime_api.model.database import db
from flask_anime_api.user.repository import UserRepository
from flask_anime_api.model.schemas import UserDTO, UserCreateSchema, UserUpdateSchema

class UserService():
    def __init__(self):
        self.user_repo = UserRepository(db)

    def get_by_id(self, user_id: UUID) -> UserDTO:
        try:
            u = self.user_repo.get_by_id(user_id)
        except:
            raise

        if u.is_deleted:
            return None

        return u

    def get_all(self) -> list[UserDTO]:
        try:
            users = self.user_repo.get_all()
        except:
            raise

        return users
        
    
    def create(self, user_data: UserCreateSchema) -> UserDTO:
        try:
            u = self.user_repo.create(user_data)
        except:
            raise
        
        return u

    def update(self, user_id: UUID, user_data: UserUpdateSchema) -> UserDTO:
        try:
            u = self.user_repo.update(user_id, user_data)
        except:
            raise
        
        return u

    def delete(self):
        ...