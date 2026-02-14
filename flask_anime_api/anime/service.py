from uuid import UUID

from flask_anime_api.model.schemas import AnimeDTO, AnimeResponseScheme, StudioDTO, StudioInList
from flask_anime_api.anime.repository import AnimeRepository
from flask_anime_api.studio.repository import StudioRepository


class AnimeService:
    def __init__(self):
        self.anime_repo = AnimeRepository()
        self.studios_repo = StudioRepository()

    def __get_anime_studios(self, a: AnimeDTO, studios: StudioDTO) -> list[StudioInList]:
        data = []
        for s in studios:
            if s.id in a.studios_ids:
                data.append(StudioInList(id=s.id, name=s.name))
        return data

    def get_all(self) -> list[AnimeResponseScheme]:
        anime = self.anime_repo.get_all()
        studios = self.studios_repo.get_all()
        
        data = []
        for a in anime:
            anime_studios = self.__get_anime_studios(a, studios)
            data.append(AnimeResponseScheme(
                id=a.id,
                title=a.title,
                episodes=a.episodes,
                studios=anime_studios
            ))

        return data 

    def get_by_id(self, id_: UUID) -> AnimeResponseScheme:
        """
        Raises value error if no such id
        """
        a = self.anime_repo.get_by_id(id_)
        
        if (a is None) or a.is_deleted:
            raise ValueError("no such id")
        
        studios = self.studios_repo.get_all()
        studios_resp = []
        for s in studios:
            if s.id in a.studios_ids:
                studios_resp.append({'id': s.id, 'name': s.name})

        return AnimeResponseScheme(
            id=a.id,
            title=a.title,
            episodes=a.episodes,
            studios=studios_resp
        )
    