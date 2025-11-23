from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from app.models.task import Task, TaskStatus


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


class InMemoryTaskRepository(TaskRepository):

    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task):
        self.tasks.append(task)

    def task_exists(self, task_id: str) -> bool:
        return any(task.id == task_id for task in self.tasks)

    def get_task(self, task_id: str) -> Optional[Task]:
        return next((task for task in self.tasks if task.id == task_id), None)

    def update_task(
            self,
            project_id: str,
            task_id: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
            status: Optional[TaskStatus] = None,
            deadline: Optional[datetime] = None
    ) -> bool:

        task = self.get_task(task_id)
        if task is None:
            return False

        if title is not None:
            task.name = title
        if description is not None:
            task.description = description
        if status is not None:
            task.status = status
        if deadline is not None:
            task.deadline = deadline

        return True

    def delete_task(self, task_id: str):
        for t in self.tasks:
            if t.id == task_id:
                self.tasks.remove(t)

    def get_project_tasks(self, project_id: str) -> List[Task]:
        return [task for task in self.tasks if task.project_id == project_id]
