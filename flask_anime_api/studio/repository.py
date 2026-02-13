from uuid import UUID
from datetime import datetime, timezone

from sqlalchemy import select, update

from flask_anime_api.model.database import db
from flask_anime_api.model.studio import Studio
from flask_anime_api.model.schemas import StudioDTO, StudioCreateSchema

class StudioRepository:
    def __init__(self):
        self.database = db

    def get_by_id(self, id_: UUID) -> StudioDTO:
        with db.session_scope() as s:
            studio = s.get(Studio, id_)
            if not studio:
                raise ValueError('No such studio')

            return StudioDTO(**studio.to_dict())
            
    def get_all(self) -> list[StudioDTO]:
        with db.session_scope() as s:
            studios = s.scalars(select(Studio)).all()
            return [
                StudioDTO(**studio.to_dict()) for studio in studios
            ]
    
    def create(self, studio_data: StudioCreateSchema) -> StudioDTO:
        with self.database.session_scope() as s:
            studio = Studio(**studio_data.model_dump())
            s.add(studio)
            s.flush([studio])
            return StudioDTO(**studio.to_dict())

    def update(self, id_: UUID, studio_data: StudioDTO) -> StudioDTO:
        with self.database.session_scope() as s:
            studio = s.get(Studio, id_)
            if not studio:
                raise ValueError(f'No studio with id {id_}')
            
            update_values = {}
            for k, v in studio_data.model_dump().items():
                if getattr(studio, k) != v:
                    update_values[k] = v
            
            if update_values == {}:
                return StudioDTO(**studio.to_dict())

            s.execute(update(Studio)
                      .where(Studio.id == id_)
                      .values(**update_values)
            )
            s.flush([studio])
            s.refresh(studio)

            return StudioDTO(**studio.to_dict())
        
    def delete(self, id_: UUID) -> None:
        with self.database.session_scope() as s:
            studio = s.get(Studio, id_)

            if (studio is None) or (studio.is_deleted):
                raise ValueError

            studio.is_deleted = True
            studio.deleted_at = datetime.now(timezone.utc)
