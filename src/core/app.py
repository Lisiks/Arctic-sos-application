from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.exc import IntegrityError, DBAPIError

from .exc_handlers import set_exc_handlers

from ..web import router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Приложение для регистрации и учета сигналов бедствий на арктических станциях.",
        version="1.0.0",
    )
    app.include_router(router)
    app.mount("/static", StaticFiles(directory="src/static"), name="static")

    set_exc_handlers(app)

    return app



