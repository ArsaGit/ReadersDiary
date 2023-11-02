from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.models import base_models


class Status(base_models.Base):
    __tablename__ = "status"

    status: Mapped[str] = mapped_column(primary_key=True)
