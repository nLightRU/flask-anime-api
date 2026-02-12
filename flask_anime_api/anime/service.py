from uuid import UUID
from flask_anime_api.anime.repository import AnimeRepository

from flask_anime_api.model.schemas import AnimeDTO

class AnimeService:
    def __init__(self, repo: AnimeRepository):
        self.repository = repo

    def get_all(self) -> list[AnimeDTO]:
        return self.repository.get_all()
    

    def get_by_id(self, _id: UUID | str):
        """
        Raises value error if no such id
        """
        a = self.repository.get_by_id(_id)
        if not a:
            raise ValueError("no such id")
        
        return a
