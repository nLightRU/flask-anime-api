from uuid import UUID, uuid4

from flask_anime_api.model.schemas import AnimeDTO, AnimeCreateScheme
from flask_anime_api.data import anime_data

class AnimeRepository:
    def __init__(self):
        self.repo_data = anime_data

    def get_by_id(self, _id: UUID | str) -> AnimeDTO | None:
        if isinstance(_id, str):
            _id = UUID(_id)
            
        for d in self.repo_data:
            if d['id'] == _id:
                return AnimeDTO(**d)
        
        return None
    

    def get_all(self) -> list[AnimeDTO]: 
        return [
            AnimeDTO(**d) for d in self.repo_data
        ]
    
    
    def create(self, anime_data: AnimeCreateScheme) -> AnimeDTO | None:
        new_id = uuid4()
        d = anime_data.model_dump()
        d['id'] = new_id
        self.repo_data.append(d)
        return AnimeDTO(**d)