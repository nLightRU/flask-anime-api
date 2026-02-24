from uuid import UUID

from flask_anime_api.model.schemas import AnimeDTO, AnimeResponseScheme, AnimeUpdateScheme, StudioDTO, BaseEntityInList
from flask_anime_api.anime.repository import AnimeRepository
from flask_anime_api.studio.repository import StudioRepository


class AnimeService:
    def __init__(self):
        self.anime_repo = AnimeRepository()
        self.studios_repo = StudioRepository()

    def get_all(self) -> list[AnimeResponseScheme]:
        try:
            anime = self.anime_repo.get_all()
        except:
            raise

        data = []
        for a in anime:
            data.append(AnimeResponseScheme(**a.model_dump()))

        return data 

    def get_by_id(self, id_: UUID) -> AnimeResponseScheme | None:
        try:
            a = self.anime_repo.get_by_id(id_)
        except:
            raise

        if (a is None) or a.is_deleted:
            return None

        return AnimeResponseScheme(**a.model_dump())

    def update_anime(self, anime_id: UUID, anime_data: AnimeUpdateScheme) -> AnimeResponseScheme:
        a = self.anime_repo.update(anime_id, anime_data)
        if not a:
            return None

        return AnimeResponseScheme(**a.model_dump())
