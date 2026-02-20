from uuid import UUID

from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash

from flask_anime_api.model.base import Base

class User(Base):
    __tablename__ = 'users'
    
    id_: Mapped[UUID] = mapped_column('id', primary_key=True, server_default=text('gen_random_uuid()'))
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id_,
            'username': self.username,
            'email': self.email
        }