from uuid import UUID
from pydantic import BaseModel


class AnimeDTO(BaseModel):
    id: UUID
    title: str
    episodes: int


class AnimeCreateScheme(BaseModel):
    title: str
    episodes: int