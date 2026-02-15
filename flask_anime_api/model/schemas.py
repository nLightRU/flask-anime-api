from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel

class BaseStudio(BaseModel):
    name: str
    description: str | None = None
    established: date | None = None
    website: str | None = None


class StudioInList(BaseModel):
    id: UUID
    name: str


class AnimeDTO(BaseModel):
    id: UUID
    title: str
    episodes: int
    is_deleted: bool = False
    studios_ids: list[UUID] | None = None


class AnimeResponseScheme(BaseModel):
    id: UUID
    title: str 
    episodes: int | None  = None
    studios: list[StudioInList] | None = None


class AnimeCreateScheme(BaseModel):
    title: str
    episodes: int


class StudioDTO(BaseStudio):
    id: UUID
    is_deleted: bool = False
    deleted_at: datetime | None = None
