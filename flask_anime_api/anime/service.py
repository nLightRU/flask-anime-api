from uuid import UUID

from flask_anime_api.model.schemas import AnimeDTO, AnimeResponseScheme

from flask_anime_api.anime.repository import AnimeRepository
from flask_anime_api.studio.repository import StudioRepository


class AnimeService:
    def __init__(self):
        self.anime_repo = AnimeRepository()
        self.studios_repo = StudioRepository()

    def get_all(self) -> list[AnimeDTO]:
        return self.repository.get_all()
    
    def get_by_id(self, id_: UUID | str) -> AnimeResponseScheme:
        """
        Raises value error if no such id
        """

        a = self.anime_repo.get_by_id(id_)
        if not a or a.is_deleted:
            raise ValueError("no such id")
        
        studios = self.studios_repo.get_all()
        studios_resp = []
        for s in studios:
            if s.id in a.studios_ids:
                studios_resp.append({'id': s.id, 'name': s.name})

        return AnimeResponseScheme(
            id=a.id,
            titile=a.title,
            episodes=a.episodes,
            studios=studios_resp
        )

    def get_all(self, id_: UUID | str) -> list[AnimeResponseScheme]:
        ...
