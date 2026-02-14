from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select, update

from flask_anime_api.model.schemas import AnimeDTO, AnimeCreateScheme
from flask_anime_api.model.database import db
from flask_anime_api.model.anime import Anime

class AnimeRepository:
    def __init__(self):
        self.database = db

    def get_by_id(self, id_ : UUID | str) -> AnimeDTO:
        with self.database.session_scope() as s:
            a = s.get(Anime, id_)
            studios_id = [studio.id for studio in a.studios]
            
            if not a:
                raise ValueError('no such id')
            
            return AnimeDTO(**a.to_dict(), studios_ids=studios_id)

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
    
    def update(self, id_, data: AnimeDTO) -> AnimeDTO:
        with self.database.session_scope() as s:
            a = s.get(Anime, id_)
            if not a:
                raise ValueError('no such id')
            update_values = {}
            for k, v in data.model_dump().items():
                if getattr(a, k) != v:
                    update_values[k] = v
            
            if update_values == {}:
                return AnimeDTO(**a.to_dict())

            s.execute(
                update(Anime)
                .where(Anime.id == id_)
                .values(**update_values)
            )

            s.flush([a])
            s.refresh(a)
            return AnimeDTO(**a.to_dict())
        
    def delete(self, id_):
        with self.database.session_scope() as s:
            a = s.get(Anime, id_)
            if not a:
                raise ValueError
            if a.is_deleted:
                raise ValueError

            a.is_deleted = True
            a.deleted_at = datetime.now(timezone.utc)