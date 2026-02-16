from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

class BaseEntityInList(BaseModel):
    id: UUID
    name: str

class BaseAnime(BaseModel):
    title: str
    episodes: int | None = None


class AnimeDTO(BaseAnime):
    id: UUID
    is_deleted: bool = False
    deleted_at: datetime | None
    studios_ids: list[UUID] | None = None


class AnimeResponseScheme(BaseAnime):
    id: UUID
    title: str 
    episodes: int | None  = None
    studios: list[BaseEntityInList] | None = None


class AnimeUpdateScheme(BaseAnime):
    studios_ids: list[UUID]


class BaseStudio(BaseModel):
    name: str
    description: str | None = None
    established: date | None = None
    website: str | None = None


class StudioDTO(BaseStudio):
    id: UUID
    is_deleted: bool = False
    deleted_at: datetime | None = None
