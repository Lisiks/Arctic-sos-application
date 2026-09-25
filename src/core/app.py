from fastapi import FastAPI

def create_app() -> FastAPI:
    app = FastAPI(
        title="Приложение для регистрации и учета сигналов бедствий на арктических станциях.",
        version="1.0.0",
    )
    return app