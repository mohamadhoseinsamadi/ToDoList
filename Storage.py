from datetime import datetime
from typing import Dict, List, Optional

from models import Project,TaskStatus,Task

class Memory:
    def __init__(self):
        self.projects: Dict[str, Project] = {}
        self.tasks: Dict[str, Task] = {}
        self.project_tasks: Dict[str, List[str]] = {}

    def add_project(self, project: Project) -> None:
        self.projects[project.id] = project
        self.project_tasks[project.id] = []

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.projects.get(project_id)

    def get_all_projects(self) -> List[Project]:
        return sorted(self.projects.values(), key=lambda p: getattr(p, "created_at", datetime.min))

    def update_project(self, project_id: str, name: str, description: str) -> bool:
        if project_id in self.projects:
            self.projects[project_id].name = name
            self.projects[project_id].description = description
            return True
        return False

    def delete_project(self, project_id: str) -> bool:
        if project_id in self.projects:
            task_ids = self.project_tasks.get(project_id, [])
            for tid in list(task_ids):
                if tid in self.tasks:
                    del self.tasks[tid]
            del self.project_tasks[project_id]
            del self.projects[project_id]
            return True
        return False

    def project_exists(self, name: str) -> bool:
        return any(p.name == name for p in self.projects.values())

    def add_task(self, task: Task) -> None:
        self.tasks[task.id] = task
        if task.project_id not in self.project_tasks:
            self.project_tasks[task.project_id] = []
        self.project_tasks[task.project_id].append(task.id)

    def get_task(self, task_id: str) -> Optional[Task]:
        return self.tasks.get(task_id)

    def get_project_tasks(self, project_id: str) -> List[Task]:
        task_ids = self.project_tasks.get(project_id, [])
        tasks = [self.tasks[task_id] for task_id in task_ids if task_id in self.tasks]
        return sorted(tasks, key=lambda t: getattr(t, "created_at", datetime.min))

    def update_task(self, task_id: str, title: str, description: str, status: str):
        pass