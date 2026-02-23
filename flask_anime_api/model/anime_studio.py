from sqlalchemy import ForeignKey, Table, Column
from flask_anime_api.model.base import Base

anime_studio_table = Table(
    'anime_studios',
    Base.metadata,
    Column('anime_id', ForeignKey('anime.id', ondelete='cascade'), primary_key=True),
    Column('studio_id', ForeignKey('studios.id', ondelete='cascade'), primary_key=True),
)
