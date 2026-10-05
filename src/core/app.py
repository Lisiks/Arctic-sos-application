from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError, DBAPIError
from contextlib import asynccontextmanager

from .exc_handlers import set_exc_handlers
from .database import session_fabric
from ..database.repositories.users_repository import UsersRepository
from ..models.users_models import UserPostModel
from ..enums import UserRoles
from .settings import config

from ..web import router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with session_fabric() as session:
        repository = UsersRepository(session)
        await repository.create_superuser()

    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Приложение для регистрации и учета сигналов бедствий на арктических станциях.",
        version="1.0.0",
        lifespan=lifespan
    )
    app.include_router(router)
    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    set_exc_handlers(app)

    return app



