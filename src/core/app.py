from fastapi import FastAPI

from ..web import router

def create_app() -> FastAPI:
    app = FastAPI(
        title="Приложение для регистрации и учета сигналов бедствий на арктических станциях.",
        version="1.0.0",
    )
    app.include_router(router)

    return app