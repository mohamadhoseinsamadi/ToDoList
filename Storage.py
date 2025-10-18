from datetime import datetime
from typing import Dict, List, Optional
from models import Project, TaskStatus, Task


class Memory:
    def __init__(self):
        self.projects: list[Project] = []

    def find_project_index(self, project_id: str) -> int:
        for idx, project in enumerate(self.projects):
            if project.id == project_id:
                return idx
        return -1

    def add_project(self, project: Project) -> None:
        self.projects.append(project)

    def edite_project_name(self, project: Project, new_name: str) -> bool:
        idx = self.find_project_index(project.id)
        if idx != -1:
            self.projects[idx].name = new_name
            return True
        return False

    def delete_project(self, project_id: str) -> bool:
        idx = self.find_project_index(project_id)
        if idx != -1:

            del self.projects[idx]
            return True
        return False

    def get_project(self, project_id: str) -> Optional[Project]:
        idx = self.find_project_index(project_id)
        if idx != -1:
            return self.projects[idx]
        return None

    def get_all_projects(self) -> List[Project]:
        return self.projects

    def project_exists(self, name: str) -> bool:
        return any(p.name.lower() == name.lower() for p in self.projects)

    def add_task_to_project(self, project_id: str, task: Task) -> bool:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return False
        self.projects[idx].tasks.append(task)
        return True

    def get_project_tasks(self, project_id: str) -> List[Task]:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return []
        return sorted(self.projects[idx].tasks, key=lambda t: getattr(t, "created_time", datetime.min))

    def update_task(self, project_id: str, task_id: str, *, title: Optional[str] = None,
                    description: Optional[str] = None, status: Optional[str] = None) -> bool:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return False
        tasks = self.projects[idx].tasks
        for t in tasks:
            if t.id == task_id:
                if title is not None:
                    t.name = title
                if description is not None:
                    t.description = description
                if status is not None:
                    t.status = status
                return True
        return False
