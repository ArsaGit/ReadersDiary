from fastapi import FastAPI, Depends

from app.utils.init_db import init_db
from app.routers.users import users_router
from app.routers.auth import auth_router
from app.services.auth import get_current_active_user


def create_app():
    init_db()
    app = FastAPI(title="My api",
                  docs_url="/api/docs",
                  openapi_url="/api")

    app.include_router(users_router,
                       tags=["users"],
                       prefix="/api",
                       dependencies=[Depends(get_current_active_user)])
    app.include_router(auth_router, prefix="/api", tags=["auth"])

    return app


app = create_app()
