from uuid import UUID

from flask_anime_api.model.schemas import BaseStudio, StudioDTO 
from flask_anime_api.studio.repository import StudioRepository
from flask_anime_api.anime.repository import AnimeRepository


class StudioService:
    def __init__(self):
        self.anime_repo = AnimeRepository()
        self.studio_repo = StudioRepository()
    
    def get_by_id(self, id_: UUID) -> StudioDTO:
        try:
            studio = self.studio_repo.get_by_id(id_)
        except:
            raise

        if studio is None or studio.is_deleted:
            return None
        
        return studio
    
    def get_all(self):
        try:
            studios = self.studio_repo.get_all()
        except:
            raise

        return studios

    def create(self, studio_data: BaseStudio):
        try:
            studio = self.studio_repo.create(studio_data)
        except:
            raise

        return studio

    def update(self, id_: UUID, studio_data: BaseStudio):
        try:
            studio = self.studio_repo.update(id_, studio_data)
        except:
            raise
        
        return studio
        
    def delete(self, id_: UUID) -> bool:
        try:
            self.studio_repo.delete(id_)
        except:
            raise
        
        return True