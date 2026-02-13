from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column

from flask_anime_api.model.base_model import Base

class Anime(Base):
    __tablename__ = 'anime'

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column()
    episodes: Mapped[int] = mapped_column(nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'episodes': self.episodes
        }