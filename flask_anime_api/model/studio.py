from datetime import date, datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flask_anime_api.model.anime import Anime
from flask_anime_api.model.base import Base
from flask_anime_api.model.anime_studio import anime_studio_table

if TYPE_CHECKING:
    from .anime import Anime

class Studio(Base):
    __tablename__ = 'studios'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str] = mapped_column()
    established: Mapped[date] = mapped_column(Date, nullable=True)
    description: Mapped[str] = mapped_column(nullable=True)
    website: Mapped[str] = mapped_column(nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=True)

    anime: Mapped[list["Anime"]] = relationship(secondary=anime_studio_table,
                                                back_populates='studios')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'established': self.established,
            'description': self.description,
            'website': self.website,
            'is_deleted': self.is_deleted,
            'deleted_at': self.deleted_at,
        }