from typing import (
    List,
    Optional,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models import base_models, review_models


class User(base_models.Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True,
                                    autoincrement=True,
                                    index=True)
    email: Mapped[str] = mapped_column(unique=True,
                                       index=True,
                                       nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[Optional[str]] = mapped_column(unique=True,
                                                    nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    reviews: Mapped[List["review_models.Review"]] = relationship(
        back_populates="user",
    )
