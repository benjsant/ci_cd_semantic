from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from app.database import engine
from app.routes import items_router


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI) -> AsyncGenerator[None]:
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(
    title="Items CRUD API",
    description="API pour gérer une liste d'articles",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(items_router)


@app.get("/")
def root() -> dict:
    return {"message": "Items CRUD API"}


@app.get("/health")
def health() -> dict:
    try:
        from sqlmodel import text

        from app.database import engine

        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "healthy", "database": "connected"}
    except Exception:
        return {"status": "degraded", "database": "disconnected"}
