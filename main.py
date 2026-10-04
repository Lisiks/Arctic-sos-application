from src.core import create_app, config
import uvicorn


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=config.app.port)
