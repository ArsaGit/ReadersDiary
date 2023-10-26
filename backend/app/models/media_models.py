from datetime import datetime
from typing import Optional, List

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.models import (
    base_models,
    attachment_models,
    review_models,
)


class Media(base_models.Base):
    __tablename__ = "medias"

    id: Mapped[str] = mapped_column(primary_key=True)
    media_type: Mapped[str]
    title: Mapped[str]
    status: Mapped[str] = mapped_column(ForeignKey("statuses.status"))
    description: Mapped[str]
    cover_id: Mapped[Optional[str]] = mapped_column(ForeignKey("images.id"))
    release_date: Mapped[datetime]

    cover: Mapped["attachment_models.Image"] = relationship()
    reviews: Mapped[List["review_models.Review"]] = relationship(
        back_populates="media"
    )

    __mapper_args__ = {
        "polymorphic_identity": "media",
        "polymorphic_on": "media_type",
    }


class Book(Media):
    __tablename__ = "books"

    id: Mapped[str] = mapped_column(ForeignKey("medias.id"), primary_key=True)
    n_pages: Mapped[int]
    n_chapters: Mapped[int]
    author_id: Mapped[str] = mapped_column(ForeignKey("authors.id"))

    author: Mapped["Author"] = relationship(back_populates="books")

    __mapper_args__ = {
        "polymorphic_identity": "book",
        # "inherit_condition": id == Media.id
    }


class Movie(Media):
    __tablename__ = "movies"

    id: Mapped[str] = mapped_column(ForeignKey("medias.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "movie",
        # "inherit_condition": id == Media.id
    }


class Series(Media):
    __tablename__ = "series"

    id: Mapped[str] = mapped_column(ForeignKey("medias.id"), primary_key=True)
    n_seasons: Mapped[int]

    seasons: Mapped[List["Season"]] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "series",
        # "inherit_condition": id == Media.id
    }


class Season(base_models.Base):
    __tablename__ = "seasons"

    id: Mapped[str] = mapped_column(primary_key=True)
    series_id: Mapped[str] = mapped_column(ForeignKey("medias.id"))
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[str] = mapped_column(ForeignKey("statuses.status"))
    n_episodes: Mapped[int]


class Author(base_models.Base):
    __tablename__ = "authors"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]

    books: Mapped[List["Book"]] = relationship(back_populates="author")


class Genre(base_models.Base):
    __tablename__ = "genres"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
