from uuid import UUID

from flask_anime_api.model.schemas import (
    AnimeCreateScheme,
    AnimeUpdateScheme,
    AnimeResponseScheme
)
from flask_anime_api.anime.repository import AnimeRepository
from flask_anime_api.studio.repository import StudioRepository

#TODO return AnimeDTO from all AnimeService methods

class AnimeService:
    def __init__(self):
        self.anime_repo = AnimeRepository()
        self.studios_repo = StudioRepository()

    def get_all(self, limit: int = 0, offset: int = 10) -> list[AnimeResponseScheme]:
        try:
            anime, total = self.anime_repo.get_all(limit=limit, offset=offset)
        except:
            raise

        anime_list = []
        for a in anime:
            anime_list.append(AnimeResponseScheme(**a.model_dump()))

        return anime_list, total

    def get_by_id(self, id_: UUID) -> AnimeResponseScheme | None:
        try:
            a = self.anime_repo.get_by_id(id_)
        except:
            raise

        if (a is None) or a.is_deleted:
            return None

        return AnimeResponseScheme(**a.model_dump())

    def create_anime(self, data: AnimeCreateScheme) -> AnimeResponseScheme:
        try:
            a = self.anime_repo.create(data)
        except:
            raise

        return AnimeResponseScheme(**a.model_dump())

    def update_anime(self, anime_id: UUID, anime_data: AnimeUpdateScheme) -> AnimeResponseScheme:
        a = self.anime_repo.update(anime_id, anime_data)
        if not a:
            return None

        return AnimeResponseScheme(**a.model_dump())
