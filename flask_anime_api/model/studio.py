from datetime import date
from uuid import UUID, uuid4
from sqlalchemy import Date
from sqlalchemy.orm import Mapped, mapped_column

from flask_anime_api.model.base_model import Base


class Studio(Base):
    __tablename__ = 'studios'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column()
    established: Mapped[date] = mapped_column(nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    website: Mapped[str] = mapped_column(nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'established': self.established,
            'description': self.description,
            'website': self.website
        }