from uuid import UUID

from flask_anime_api.studio.repository import StudioRepository
from flask_anime_api.anime.repository import AnimeRepository


class StudioService:
    def __init__(self):
        self.anime_repo = AnimeRepository()
        self.studio_repo = StudioRepository()
    
    def get_by_id(self, id_: UUID):
        try:
            studio = self.studio_repo.get_by_id(id_)
        except:
            raise

        if studio is None or studio.is_deleted:
            return None
        
        return NotImplementedError
    
    def get_all(self):
        ...

    def update(self, id_: UUID, studio_data):
        ...

    def delete(self, id_: UUID):
        ...