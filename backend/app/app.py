from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from app.utils.init_db import init_db
from app.routers.users import users_router
from app.routers.auth import auth_router
from app.routers.health import health_router
from app.services.auth_service import get_current_active_user


def create_app():
    init_db()
    app = FastAPI(title="My api",
                  docs_url="/api/docs",
                  openapi_url="/api",)

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(users_router,
                       tags=["users"],
                       prefix="/api",
                       dependencies=[Depends(get_current_active_user)])
    app.include_router(auth_router, prefix="/api", tags=["auth"])
    app.include_router(health_router, prefix="/api", tags=["health"])

    return app


app = create_app()
