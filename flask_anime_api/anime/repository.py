from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select, update, func

from flask_anime_api.model.schemas import ( 
    BaseEntityInList,
    BaseAnime,
    AnimeDTO,
    AnimeCreateScheme,
    AnimeUpdateScheme
)
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
            
            studios = [BaseEntityInList(id=s.id, name=s.name) for s in a.studios]
            
            return AnimeDTO(**a.to_dict(), studios=studios)

    def get_all(self, limit: int = 10, offset: int = 0) -> list[AnimeDTO]:
        with self.database.session_scope() as s:
            # total = s.execute(func.count(select(Anime.id))).scalar()
            total = -10

            query = select(Anime).order_by(Anime.id)
            if limit:
                query = query.limit(limit=limit)
            if offset:
                query = query.offset(offset=offset)

            anime = s.scalars(query).all()
            data = []
            for a in anime:
                studios = [BaseEntityInList(id=s.id, name=s.name) for s in a.studios]
                data.append(AnimeDTO(**a.to_dict(), studios=studios))

            return data, total
    
    def create(self, data: AnimeCreateScheme) -> AnimeDTO: 
        with self.database.session_scope() as s:
            anime_data = BaseAnime(**data.model_dump())
            a = Anime(**anime_data.model_dump())
            s.add(a)
            s.flush()

            if data.studios:
                stmt = select(Studio).where(Studio.id.in_(data.studios))
                studios = set(s.execute(stmt).scalars().all())
                a.studios = studios
                studios = [BaseEntityInList(id=s.id, name=s.name) for s in a.studios]
                return AnimeDTO(**a.to_dict(), studios=studios)

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
                    
            # If no base fields like title or episodes is updated
            # update querry is not executed
            if update_values:
                sess.execute(
                    update(Anime)
                    .where(Anime.id == id_)
                    .values(**update_values)
                )
                sess.refresh(a)

            # Check for studio updates
            stmt = select(Studio).where(Studio.id.in_(data.studios_ids))
            new_studios = set(sess.scalars(stmt).all())
            if a.studios != new_studios:
                print('studios updated')
                a.studios = new_studios
                sess.refresh(a)
            
            studios = [BaseEntityInList(id=s.id, name=s.name) for s in a.studios]

            return AnimeDTO(**a.to_dict(), studios=studios)
        
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