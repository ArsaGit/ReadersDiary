from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from app.routers.health import router as health_router
from app.routers.user import router as user_router
from app.utils.logging import AppLogger
from app.configs.redis import get_redis
from app.services.auth import AuthBearer

logger = AppLogger.__call__().get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the redis connection
    app.state.redis = await get_redis()
    yield
    # close redis connection and release the resources
    app.state.redis.close()


def create_app():
    app = FastAPI(title="My api", lifespan=lifespan)

    app.include_router(health_router,
                       prefix="/v1/public/health",
                       tags=["Health, Public"])
    app.include_router(health_router,
                       prefix="/v1/health",
                       tags=["Health, Bearer"],
                       dependencies=[Depends(AuthBearer())])
    app.include_router(user_router)

    return app
