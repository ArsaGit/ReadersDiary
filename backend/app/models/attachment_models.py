from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.models import base_models


class Image(base_models.Base):
    __tablename__ = "image"

    id: Mapped[str] = mapped_column(primary_key=True)
    path: Mapped[str]
