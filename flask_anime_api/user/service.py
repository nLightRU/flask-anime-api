from flask_anime_api.user.repository import UserRepository

class UserService():
    def __init__(self):
        self.user_repo = UserRepository()

    def get_by_id(self):
        ...

    def get_all(self):
        ...

    def update(self):
        ...

    def delete(self):
        ...