from flask_anime_api.user.repository import UserRepository
from flask_anime_api.model.database import db
from flask_anime_api.model.schemas import UserDTO, UserCreateSchema

class UserService():
    def __init__(self):
        self.user_repo = UserRepository(db)

    def get_by_id(self):
        ...

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

    def update(self):
        ...

    def delete(self):
        ...