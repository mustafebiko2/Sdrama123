from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Table, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class PublishStatus(str, Enum):
    draft = "draft"
    review = "review"
    published = "published"


user_roles = Table(
    "user_roles",
    Base.metadata,
    Column("user_id", ForeignKey("users.id"), primary_key=True),
    Column("role_id", ForeignKey("roles.id"), primary_key=True),
)


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    users: Mapped[list["User"]] = relationship(secondary=user_roles, back_populates="roles")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(160))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    roles: Mapped[list[Role]] = relationship(secondary=user_roles, back_populates="users")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Genre(Base):
    __tablename__ = "genres"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(140), unique=True, index=True)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    slug: Mapped[str] = mapped_column(String(140), unique=True, index=True)


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(280), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default=PublishStatus.draft.value)
    poster_path: Mapped[Optional[str]] = mapped_column(String(500))
    video_path: Mapped[Optional[str]] = mapped_column(String(500))
    genre_id: Mapped[Optional[int]] = mapped_column(ForeignKey("genres.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    subtitles: Mapped[list["Subtitle"]] = relationship(back_populates="movie", cascade="all, delete-orphan")
    views: Mapped[list["View"]] = relationship(back_populates="movie", cascade="all, delete-orphan")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="movie", cascade="all, delete-orphan")


class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    slug: Mapped[str] = mapped_column(String(280), unique=True, index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default=PublishStatus.draft.value)
    poster_path: Mapped[Optional[str]] = mapped_column(String(500))
    genre_id: Mapped[Optional[int]] = mapped_column(ForeignKey("genres.id"))
    category_id: Mapped[Optional[int]] = mapped_column(ForeignKey("categories.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    seasons: Mapped[list["Season"]] = relationship(back_populates="series", cascade="all, delete-orphan")


class Season(Base):
    __tablename__ = "seasons"
    __table_args__ = (UniqueConstraint("series_id", "number", name="uq_series_season_number"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    series_id: Mapped[int] = mapped_column(ForeignKey("series.id"))
    title: Mapped[str] = mapped_column(String(255))
    number: Mapped[int] = mapped_column(Integer)
    series: Mapped[Series] = relationship(back_populates="seasons")
    episodes: Mapped[list["Episode"]] = relationship(back_populates="season", cascade="all, delete-orphan")


class Episode(Base):
    __tablename__ = "episodes"
    __table_args__ = (UniqueConstraint("season_id", "number", name="uq_season_episode_number"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    season_id: Mapped[int] = mapped_column(ForeignKey("seasons.id"))
    title: Mapped[str] = mapped_column(String(255))
    number: Mapped[int] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), default=PublishStatus.draft.value)
    video_path: Mapped[Optional[str]] = mapped_column(String(500))
    poster_path: Mapped[Optional[str]] = mapped_column(String(500))
    season: Mapped[Season] = relationship(back_populates="episodes")
    subtitles: Mapped[list["Subtitle"]] = relationship(back_populates="episode", cascade="all, delete-orphan")
    views: Mapped[list["View"]] = relationship(back_populates="episode", cascade="all, delete-orphan")
    favorites: Mapped[list["Favorite"]] = relationship(back_populates="episode", cascade="all, delete-orphan")


class Subtitle(Base):
    __tablename__ = "subtitles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    language: Mapped[str] = mapped_column(String(80), default="English")
    file_path: Mapped[str] = mapped_column(String(500))
    movie_id: Mapped[Optional[int]] = mapped_column(ForeignKey("movies.id"))
    episode_id: Mapped[Optional[int]] = mapped_column(ForeignKey("episodes.id"))
    movie: Mapped[Optional[Movie]] = relationship(back_populates="subtitles")
    episode: Mapped[Optional[Episode]] = relationship(back_populates="subtitles")


class View(Base):
    __tablename__ = "views"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    movie_id: Mapped[Optional[int]] = mapped_column(ForeignKey("movies.id"))
    episode_id: Mapped[Optional[int]] = mapped_column(ForeignKey("episodes.id"))
    watched_seconds: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    movie: Mapped[Optional[Movie]] = relationship(back_populates="views")
    episode: Mapped[Optional[Episode]] = relationship(back_populates="views")


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "movie_id", "episode_id", name="uq_user_favorite_content"),)

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    movie_id: Mapped[Optional[int]] = mapped_column(ForeignKey("movies.id"))
    episode_id: Mapped[Optional[int]] = mapped_column(ForeignKey("episodes.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[User] = relationship(back_populates="favorites")
    movie: Mapped[Optional[Movie]] = relationship(back_populates="favorites")
    episode: Mapped[Optional[Episode]] = relationship(back_populates="favorites")


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    key: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    value: Mapped[str] = mapped_column(Text)
