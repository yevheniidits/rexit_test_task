from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from apps.dataset_processor.db_service import DatasetDbService
from apps.dataset_processor.router import router as dataset_router
from config.main import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    await DatasetDbService().initialize_database()
    yield


app = FastAPI(
    lifespan=lifespan,
    debug=settings.DEBUG,
    title=settings.PROJECT_NAME,
    description=f'{settings.PROJECT_NAME} API documentation',
    docs_url='/swagger',
    redoc_url=None,
    version='v1',
)

app.include_router(dataset_router)
