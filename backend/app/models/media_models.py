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
    review_models,
)


class Media(base_models.Base):
    __tablename__ = "media"

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    index=True,)
    media_type: Mapped[str]
    title: Mapped[str]
    status: Mapped[str] = mapped_column(ForeignKey("status.status"))
    description: Mapped[str]
    cover_path: Mapped[Optional[str]]
    release_date: Mapped[datetime]

    reviews: Mapped[List["review_models.Review"]] = relationship(
        back_populates="media"
    )

    __mapper_args__ = {
        "polymorphic_identity": "media",
        "polymorphic_on": "media_type",
    }


class Book(Media):
    __tablename__ = "book"

    id: Mapped[int] = mapped_column(ForeignKey("media.id"), primary_key=True)
    n_pages: Mapped[int]
    n_chapters: Mapped[int]
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"))

    author: Mapped["Author"] = relationship(back_populates="books")

    __mapper_args__ = {
        "polymorphic_identity": "book",
        # "inherit_condition": id == Media.id
    }


class Movie(Media):
    __tablename__ = "movie"

    id: Mapped[int] = mapped_column(ForeignKey("media.id"), primary_key=True)

    __mapper_args__ = {
        "polymorphic_identity": "movie",
        # "inherit_condition": id == Media.id
    }


class Series(Media):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(ForeignKey("media.id"), primary_key=True)
    n_seasons: Mapped[int]

    seasons: Mapped[List["Season"]] = relationship()

    __mapper_args__ = {
        "polymorphic_identity": "series",
        # "inherit_condition": id == Media.id
    }


class Season(base_models.Base):
    __tablename__ = "season"

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    index=True,)
    series_id: Mapped[int] = mapped_column(ForeignKey("media.id"))
    title: Mapped[str]
    description: Mapped[str]
    status: Mapped[str] = mapped_column(ForeignKey("status.status"))
    n_episodes: Mapped[int]


class Author(base_models.Base):
    __tablename__ = "author"

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    index=True,)
    name: Mapped[str]

    books: Mapped[List["Book"]] = relationship(back_populates="author")


class Genre(base_models.Base):
    __tablename__ = "genre"

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    index=True,)
    name: Mapped[str] = mapped_column(unique=True)


class Tag(base_models.Base):
    __tablename__ = "tag"

    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    index=True,)
    name: Mapped[str] = mapped_column(unique=True)
