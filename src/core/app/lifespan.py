from contextlib import asynccontextmanager
from ..connections.connection import Connection
from ..connections.database.postgres_connection import postgres
from ..logger.logger import logger


@asynccontextmanager
async def lifespan(app):
    logger.info("Starting up the application...")
    await startup(postgres)
    logger.info("Application started up successfully.")
    yield
    logger.info("Shutting down the application...")
    await shutdown(postgres)
    logger.info("Application shut down successfully.")


async def startup(app: Connection):
    await app.connect()


async def shutdown(app: Connection):
    await app.close()

