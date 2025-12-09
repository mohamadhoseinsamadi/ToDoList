from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from sqlalchemy import select

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

    @abstractmethod
    def get_overdue_tasks(self, current_time: datetime) -> List[Task]:
        pass

    @abstractmethod
    def autoclose_overdue_tasks(self, current_time: datetime) -> int:
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

    def get_overdue_tasks(self, current_time: datetime) -> List[Task]:
        """
        Get all tasks that are overdue and not completed.

        Args:
            current_time: Current datetime to compare against deadlines.

        Returns:
            List of overdue tasks.
        """
        stmt = (
            select(Task)
            .where(
                Task.deadline.isnot(None),
                Task.deadline < current_time,
                Task.status != TaskStatus.DONE,
                Task.closed_at.is_(None)
            )
        )
        result = self.session.scalars(stmt).all()
        return list(result)

    def autoclose_overdue_tasks(self, current_time: datetime) -> int:
        """
        Automatically close all overdue tasks.

        Args:
            current_time: Current datetime.

        Returns:
            Number of tasks that were closed.
        """
        overdue_tasks = self.get_overdue_tasks(current_time)
        closed_count = 0

        for task in overdue_tasks:
            task.status = TaskStatus.DONE
            task.closed_at = current_time
            closed_count += 1

        if closed_count > 0:
            self.session.commit()

        return closed_count
