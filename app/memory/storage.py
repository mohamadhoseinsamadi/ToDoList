from datetime import datetime
from typing import List, Optional
from app.models.models import Project, Task, TaskStatus

class Memory:
    def __init__(self):
        self.projects: List[Project] = []

    def find_project_index(self, project_id: str) -> int:
        for idx, project in enumerate(self.projects):
            if project.id == project_id:
                return idx
        return -1

    def add_project(self, project: Project) -> None:
        self.projects.append(project)

    def edit_project_name(self, project_id: str, new_name: str) -> bool:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return False
        self.projects[idx].name = new_name
        return True

    def edit_project_description(self, project_id: str, new_desc: str) -> bool:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return False
        self.projects[idx].description = new_desc
        return True

    def delete_project(self, project_id: str) -> bool:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return False
        self.projects[idx].tasks.clear()
        self.projects.pop(idx)

        return True

    def get_project(self, project_id: str) -> Optional[Project]:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return None
        return self.projects[idx]

    def get_all_projects(self) -> List[Project]:
        return self.projects

    def project_exists(self, name: str) -> bool:
        return any(p.name.lower() == name.lower() for p in self.projects)

    def add_task_to_project(self, project_id: str, task: Task) -> bool:
        project = self.get_project(project_id)
        if project is None:
            return False
        project.tasks.append(task)
        return True

    def get_project_tasks(self, project_id: str) -> List[Task]:
        project = self.get_project(project_id)
        return project.tasks if project else []

    def update_task(
        self,
        project_id: str,
        task_id: str,
        title: Optional[str] = None,
        description: Optional[str] = None,
        status: Optional[str] = None
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
                    try:
                        t.status = TaskStatus(status)
                    except ValueError:
                        return False
                return True

        return False

    def delete_task(self, task_id: str) -> bool:
        for proj in self.projects:
            for i, t in enumerate(proj.tasks):
                if t.id == task_id:
                    del proj.tasks[i]
                    return True
        return False