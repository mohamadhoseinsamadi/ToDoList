from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict
from app.models.project import Project
from app.models.task import Task, TaskStatus


class TaskRepository(ABC):
    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
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
    def get_project(self, project_id: str) -> Optional[Project]:
        pass

    @abstractmethod
    def find_project_index(self, project_id: str) -> int:
        pass


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.projects: List[Project] = []

    def find_project_index(self, project_id: str) -> int:
        for idx, project in enumerate(self.projects):
            if project.id == project_id:
                return idx
        return -1

    def get_project(self, project_id: str) -> Optional[Project]:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return None
        return self.projects[idx]

    def update_task(
            self,
            project_id: str,
            task_id: str,
            title: Optional[str] = None,
            description: Optional[str] = None,
            status: Optional[TaskStatus] = None,
            deadline: Optional[datetime] = None
    ) -> bool:

        project = self.get_project(project_id)
        if project is None:
            return False

        for t in project.tasks:
            if t.id == task_id:
                if title is not None:
                    t.name = title
                if description is not None:
                    t.description = description
                if status is not None:
                    t.status = status
                if deadline is not None:
                    t.deadline = deadline
                return True

        return False

    def delete_task(self, task_id: str) -> bool:
        for proj in self.projects:
            for i, t in enumerate(proj.tasks):
                if t.id == task_id:
                    del proj.tasks[i]
                    return True
        return False
