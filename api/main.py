from fastapi import FastAPI
from contextlib import asynccontextmanager
import logging

from models import init_db
from routers import user, message
import config


# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title=config.NAME,
    version=config.VERSION,
    lifespan=lifespan,
    debug=config.DEBUG
)


app.include_router(user.router)
app.include_router(message.router)


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "message": f"Welcome to {config.NAME}",
        "version": config.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Проверка здоровья приложения"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True
    )
