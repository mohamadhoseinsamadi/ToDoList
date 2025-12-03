from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from app.models.task import Task, TaskStatus
from sqlalchemy.orm import Session


class TaskRepository(ABC):
    @abstractmethod
    def add_task(self, task: Task):
        pass

    @abstractmethod
    def task_exists(self, task_id: str) -> bool:
        pass

    @abstractmethod
    def delete_task(self, task_id: str):
        pass

    @abstractmethod
    def update_task(
            self,
            project_id: str,
            task_id: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
            status: Optional[TaskStatus] = None,
            deadline: Optional[datetime] = None
    ) -> bool:
        pass

    @abstractmethod
    def get_project_tasks(self, project_id: str) -> List[Task]:
        pass


class SqlAlchemyTaskRepository(TaskRepository):
    def __init__(self, session: Session):
        self.session = session

    def add_task(self, task: Task):
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

    def get_project_tasks(self, project_id: str) -> List[Task]:
        return self.session.query(Task).filter(Task.project_id == project_id).all()

    def task_exists(self, task_id: str) -> bool:
        return self.session.query(Task).filter(Task.id == task_id).first() is not None

    def delete_task(self, task_id: str):
        task = self.session.query(Task).filter(Task.id == task_id).first()
        if task:
            self.session.delete(task)
            self.session.commit()

    def update_task(self, project_id: str, task_id: str, **kwargs) -> bool:
        task = self.session.query(Task).filter(Task.id == task_id, Task.project_id == project_id).first()
        if not task:
            return False

        if 'title' in kwargs and kwargs['title']:
            task.name = kwargs['title']
        if 'description' in kwargs and kwargs['description']:
            task.description = kwargs['description']
        if 'status' in kwargs and kwargs['status']:
            task.status = kwargs['status']
        if 'deadline' in kwargs and kwargs['deadline']:
            task.deadline = kwargs['deadline']

        self.session.commit()
        return True