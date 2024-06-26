from app.config import log
from app.core.database import init_db
from app.core.dependencies import get_db
from app.config import settings

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from app.mongo.mogo import init_mongo

async def startup():
    try:
        init_db()
        init_mongo()
        redis = aioredis.from_url(settings.REDIS_URI)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    except Exception as ex:
        log.exception(f"failed to preparedb {ex}")



async def shutdown():
    log.info("shutting down")


def create_app() -> FastAPI:
    """Creating FastAPI object

    Returns:
        FastAPI:
    """
    init_db()
    _app = FastAPI()

    # region middleware

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # endregion

    # region import APIrouters from endpoints

    from app.endpoints.api import router

    _app.include_router(router)

    # add health check
    @_app.get("/health")
    async def health():
        return {"status": "ok"}

    # endregion

    # adding event handlers
    _app.add_event_handler("startup", startup)
    _app.add_event_handler("shutdown", shutdown)

    return _app
