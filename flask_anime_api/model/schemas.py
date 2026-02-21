from uuid import UUID
from datetime import date, datetime
from pydantic import BaseModel, model_serializer, EmailStr

class BaseEntityInList(BaseModel):
    id: UUID
    name: str

class BaseAnime(BaseModel):
    title: str
    type_: str | None = None
    episodes: int | None = None


class AnimeDTO(BaseAnime):
    id: UUID
    is_deleted: bool = False
    deleted_at: datetime | None
    studios: list[BaseEntityInList] | None = None


class AnimeResponseScheme(BaseAnime):
    id: UUID
    studios: list[BaseEntityInList] | None = None

    @model_serializer
    def fields_order(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type_,
            'episodes': self.episodes,
            'studios': self.studios
        }


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
    anime: list[BaseEntityInList] | None = None


class StudioResponseSchema(BaseStudio):
    id: UUID
    anime: list[BaseEntityInList] | None = None

    @model_serializer
    def fields_order(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'established': self.established,
            'website': self.website,
            'anime': self.anime
        }


class BaseUser(BaseModel):
    username: str
    email: EmailStr


class UserDTO(BaseUser):
    id: UUID
    is_active: bool | None = True
    is_admin: bool | None = False
    is_deleted: bool
    deleted_at: datetime | None


class UserCreateSchema(BaseUser):
    password: str
    is_active: bool | None = True
    is_admin: bool | None = False


class UserUpdateSchema(BaseUser):
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool
