import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from rjapi.database import database
from rjapi.loggingconf import configure_logging
from rjapi.routers.post import router as post_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    logger.info("Starting application")
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(post_router)
