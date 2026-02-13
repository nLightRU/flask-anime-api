from uuid import UUID, uuid4

from sqlalchemy import select

from flask_anime_api.model.schemas import AnimeDTO, AnimeCreateScheme
from flask_anime_api.model.database import db
from flask_anime_api.model.anime import Anime

class AnimeRepository:
    def __init__(self):
        self.database = db

    def get_by_id(self, id_ : UUID | str):
        with self.database.session_scope() as s:
            a = s.get(Anime, id_)
            
            if not s:
                raise ValueError('no such id')
            
            return AnimeDTO(**a.to_dict())

    def get_all(self) -> list[AnimeDTO]: 
        with self.database.session_scope() as s:
            anime = s.scalars(select(Anime)).all()
            return [AnimeDTO(**a.to_dict()) for a in anime]
    
    def create(self, data: AnimeCreateScheme) -> AnimeDTO: 
        with self.database.session_scope() as s:
            a = Anime(**data.model_dump())
            s.add(a)
            s.flush([a])
            return AnimeDTO(**a.to_dict())

    