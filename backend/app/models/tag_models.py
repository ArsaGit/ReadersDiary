from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.models import base_models


class Tag(base_models.Base):
    __tablename__ = "tags"

    id: Mapped[str] = mapped_column(primary_key=True)
    name: Mapped[str]
