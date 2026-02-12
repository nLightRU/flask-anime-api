from .schemas import AnimeDTO

class AnimeRepository:
    def __init__(self, repo_data):
        self.repo_data = repo_data

    def get_by_id(self, id: int) -> AnimeDTO | None:
        for d in self.repo_data:
            if d['id'] == id:
                return AnimeDTO(**d)
            
        return None
    

    def get_all(self) -> list[AnimeDTO]: 
        return [
            AnimeDTO.model_dump(d) for d in self.repo_data
        ]
        