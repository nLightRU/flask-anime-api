from uuid import UUID
from datetime import date
from pydantic import BaseModel


class AnimeDTO(BaseModel):
    id: UUID
    title: str
    episodes: int


class AnimeCreateScheme(BaseModel):
    title: str
    episodes: int


class StudioDTO(BaseModel):
    id: UUID
    name: str
    description: str | None = None
    established: date | None = None
    website: str | None = None


class StudioCreateSchema(BaseModel):
    name: str
    description: str | None = None
    established: date | None = None
    website: str | None = None