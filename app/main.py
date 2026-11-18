import uvicorn
from fastapi import FastAPI
from app.api.routers import api_router
from app.db.base import Base
from app.db.session import engine
from app.models import project, task  # noqa: F401  (register models with Base)

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ToDo List API",
    description="A RESTful API for managing projects and tasks",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)