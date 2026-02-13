from sqlalchemy import select

from flask_anime_api.model.database import db
from flask_anime_api.model.studio import Studio
from flask_anime_api.model.schemas import StudioDTO, StudioCreateSchema

class StudioRepository:
    def __init__(self):
        self.database = db

    def get_by_id(self, id_) -> StudioDTO:
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
