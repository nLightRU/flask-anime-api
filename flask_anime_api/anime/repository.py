from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select, update

from flask_anime_api.model.schemas import AnimeUpdateScheme, BaseAnime, AnimeDTO
from flask_anime_api.model.database import db
from flask_anime_api.model.anime import Anime
from flask_anime_api.model.studio import Studio

class AnimeRepository:
    def __init__(self):
        self.database = db

    def get_by_id(self, id_ : UUID) -> AnimeDTO:
        with self.database.session_scope() as s:
            a = s.get(Anime, id_)
            if not a:
                return None
            
            s_ids = [studio.id for studio in a.studios]
            
            return AnimeDTO(**a.to_dict(), studios_ids=s_ids)

    def get_all(self) -> list[AnimeDTO]:
        with self.database.session_scope() as s:
            anime = s.scalars(select(Anime)).all()
            data = []
            for a in anime:
                s_ids = [s.id for s in a.studios]
                data.append(AnimeDTO(**a.to_dict(), studios_ids=s_ids))

            return data
    
    def create(self, data: BaseAnime) -> AnimeDTO: 
        with self.database.session_scope() as s:
            a = Anime(**data.model_dump())
            s.add(a)
            s.flush([a])
            return AnimeDTO(**a.to_dict())
    
    def update(self, id_, data: AnimeUpdateScheme) -> AnimeDTO:
        with self.database.session_scope() as sess:
            a = sess.get(Anime, id_)
            if not a:
                return None
            
            update_values = {}
            for attr in BaseAnime.model_fields.keys():
                if hasattr(data, attr) and getattr(a, attr) != getattr(data, attr):
                    update_values[attr] = getattr(data, attr)
                    
            if update_values != {}:
                sess.execute(
                    update(Anime)
                    .where(Anime.id == id_)
                    .values(**update_values)
                )

            stmt = select(Studio).where(Studio.id.in_(data.studios_ids))
            new_studios = set(sess.scalars(stmt).all())
            a.studios = new_studios
            
            sess.refresh(a)
            
            studios_ids = [s.id for s in a.studios]

            return AnimeDTO(**a.to_dict(), studios_ids=studios_ids)
        
    def delete(self, id_):
        with self.database.session_scope() as s:
            a = s.get(Anime, id_)
            if not a:
                return False
            if a.is_deleted:
                return False

            a.is_deleted = True
            a.deleted_at = datetime.now(timezone.utc)

            return True