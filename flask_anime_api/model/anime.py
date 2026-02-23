"""
Модель аниме тайтла в базе данных
"""

from datetime import datetime
from uuid import UUID, uuid4
from typing import TYPE_CHECKING

from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from flask_anime_api.model.base import Base
from flask_anime_api.model.anime_studio import anime_studio_table

if TYPE_CHECKING:
    from .studio import Studio

class Anime(Base):
    __tablename__ = 'anime'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    type_: Mapped[str] = mapped_column('type', nullable=True)
    title: Mapped[str] = mapped_column()
    episodes: Mapped[int] = mapped_column(nullable=True)
    is_deleted: Mapped[bool] = mapped_column(default=False)
    deleted_at: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)

    studios: Mapped[set["Studio"]] = relationship(secondary=anime_studio_table,
                                                  back_populates='anime')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'episodes': self.episodes,
            'type': self.type_,
            'is_deleted': self.is_deleted,
            'deleted_at': self.deleted_at
        }
