from pydantic import BaseModel


class AnimeDTO(BaseModel):
    id: int
    title: str