from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.models import (
    base_models,
    media_models,
    user_models,
)


class Review(base_models.Base):
    __tablename__ = "reviews"

    id: Mapped[str] = mapped_column(primary_key=True)
    media_type: Mapped[str]
    rating: Mapped[int]
    body: Mapped[str]
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id")
    )
    media_id: Mapped[str] = mapped_column(
        ForeignKey("medias.id")
    )
    start_date: Mapped[datetime]
    end_date: Mapped[Optional[datetime]]

    user: Mapped["user_models.User"] = relationship(back_populates="reviews")
    media: Mapped["media_models.Media"] = relationship(
        back_populates="reviews"
    )

    __mapper_args__ = {
        "polymorphic_identity": "media",
        "polymorphic_on": "media_type",
    }


class BookReview(Review):
    __tablename__ = "book_reviews"

    id: Mapped[str] = mapped_column(ForeignKey("reviews.id"), primary_key=True)
    book_type: Mapped[str]

    __mapper_args__ = {
        "polymorphic_identity": "book",
        # "inherit_condition": id == Review.id
    }


# class MovieReview(Review):
#     __mapper_args__ = {
#         "polymorphic_identity": "movie",
#         "inherit_condition": id == Review.id
#     }


# class SeriesReview(Review):
#     __mapper_args__ = {
#         "polymorphic_identity": "series",
#         "inherit_condition": id == Review.id
#     }


# class SeasonReview(Review):
#     __mapper_args__ = {
#         "polymorphic_identity": "season",
#         "inherit_condition": id == Review.id
#     }
