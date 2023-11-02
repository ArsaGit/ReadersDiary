#!/usr/bin/env python3

from app.configs.database import get_init_db
from app.repositories.user import create_user_sync
from app.schemas.api.user import UserCreate


def init() -> None:
    db = get_init_db()

    create_user_sync(db, UserCreate(email="admin@mail.com",
                                    password="password",
                                    is_active=True,
                                    is_superuser=True,
                                    username="admin",))


if __name__ == "__main__":
    print("Creating superuser admin@mail.com")
    init()
    print("Superuser created")
