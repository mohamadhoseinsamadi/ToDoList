from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.repositories.project_repository import SqlAlchemyProjectRepository
from app.repositories.task_repository import SqlAlchemyTaskRepository
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


def get_db() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Yields a database session and ensures it's closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_project_service(db: Session = Depends(get_db)) -> ProjectService:
    """
    Dependency function to get ProjectService instance.
    """
    project_repo = SqlAlchemyProjectRepository(db)
    return ProjectService(project_repo)


def get_task_service(db: Session = Depends(get_db)) -> TaskService:
    """
    Dependency function to get TaskService instance.
    """
    task_repo = SqlAlchemyTaskRepository(db)
    return TaskService(task_repo)

