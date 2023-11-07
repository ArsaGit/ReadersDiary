#!/usr/bin/env python3
from sqlalchemy.orm import Session

from app.schemas.api.user import UserCreate
from app.configs.database import get_init_db
from app.models.user_models import User


def create_sync(db: Session, user_create: UserCreate) -> User:
    user_dict = user_create.model_dump()
    user = User(**user_dict)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def init() -> None:
    db = get_init_db()
    create_sync(db, UserCreate(email="admin@mail.com",
                               password="password",
                               is_active=True,
                               is_superuser=True,
                               username="admin",))


if __name__ == "__main__":
    print("Creating superuser admin@mail.com")
    init()
    print("Superuser created")
