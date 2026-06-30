from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RoleRead(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "user"


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    created_at: datetime
    roles: list[RoleRead] = []

    model_config = ConfigDict(from_attributes=True)


class TaxonomyCreate(BaseModel):
    name: str
    slug: str


class TaxonomyRead(TaxonomyCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieCreate(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    status: str = "draft"
    genre_id: Optional[int] = None
    category_id: Optional[int] = None


class MovieUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    genre_id: Optional[int] = None
    category_id: Optional[int] = None


class MovieRead(MovieCreate):
    id: int
    poster_path: Optional[str] = None
    video_path: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SeriesCreate(BaseModel):
    title: str
    slug: str
    description: Optional[str] = None
    status: str = "draft"
    genre_id: Optional[int] = None
    category_id: Optional[int] = None


class SeriesUpdate(BaseModel):
    title: Optional[str] = None
    slug: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    genre_id: Optional[int] = None
    category_id: Optional[int] = None


class SeriesRead(SeriesCreate):
    id: int
    poster_path: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SeasonCreate(BaseModel):
    title: str
    number: int


class SeasonRead(SeasonCreate):
    id: int
    series_id: int

    model_config = ConfigDict(from_attributes=True)


class EpisodeCreate(BaseModel):
    title: str
    number: int
    description: Optional[str] = None
    status: str = "draft"


class EpisodeUpdate(BaseModel):
    title: Optional[str] = None
    number: Optional[int] = None
    description: Optional[str] = None
    status: Optional[str] = None


class EpisodeRead(EpisodeCreate):
    id: int
    season_id: int
    video_path: Optional[str] = None
    poster_path: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class SubtitleRead(BaseModel):
    id: int
    language: str
    file_path: str
    movie_id: Optional[int] = None
    episode_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class ViewCreate(BaseModel):
    user_id: Optional[int] = None
    movie_id: Optional[int] = None
    episode_id: Optional[int] = None
    watched_seconds: int = 0


class FavoriteCreate(BaseModel):
    user_id: int
    movie_id: Optional[int] = None
    episode_id: Optional[int] = None


class SettingWrite(BaseModel):
    key: str
    value: str


class SettingRead(SettingWrite):
    id: int

    model_config = ConfigDict(from_attributes=True)
