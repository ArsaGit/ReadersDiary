from typing import (
    List,
    Any,
)

import bcrypt
from passlib.context import CryptContext

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.models import (
    base_models,
    review_models,
)

from app.utils.uuid import get_uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(base_models.Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    login: Mapped[str]
    _password: Mapped[bytes]
    email: Mapped[str]

    reviews: Mapped[List["review_models.Review"]] = relationship(
        back_populates="user"
    )

    @property
    def password(self):
        return self._password.decode("utf-8")

    @password.setter
    def password(self, password: str):
        self._password = bcrypt.hashpw(password.encode('utf-8'),
                                       bcrypt.gensalt())

    def check_password(self, password: str):
        return pwd_context.verify(password, self.password)

    @classmethod
    async def find(cls,
                   database_session: AsyncSession,
                   where_conditions: list[Any]):

        _stmt = select(cls).where(*where_conditions)
        _result = await database_session.execute(_stmt)
        return _result.scalars().first()

    async def save(self, db_session: AsyncSession):
        self.id = get_uuid()
        await super().save(db_session)
