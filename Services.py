import uuid
from typing import List, Optional, Tuple, Union

from models import Project, Task, TaskStatus
from config import (
    MAX_NUMBER_OF_PROJECTS,
    MAX_NUMBER_OF_TASKS,
    MAX_PROJECT_NAME_LENGTH,
    MAX_PROJECT_DESCRIPTION_LENGTH,
    MAX_TASK_NAME_LENGTH,
    MAX_TASK_DESCRIPTION_LENGTH,
)
from Storage import Memory


class ProjectTaskService:
    def __init__(self, storage: Memory):
        self.storage = storage

    def add_project(self, name: str, description: str) -> Tuple[bool, str]:
        if len(name) > MAX_PROJECT_NAME_LENGTH:
            return False, f"Project's name cannot exceed {MAX_PROJECT_NAME_LENGTH} characters"
        if len(description) > MAX_PROJECT_DESCRIPTION_LENGTH:
            return False, f"Project's description cannot exceed {MAX_PROJECT_DESCRIPTION_LENGTH} characters"
        if len(self.storage.projects) >= MAX_NUMBER_OF_PROJECTS:
            return False, f"Cannot exceed maximum number of projects: {MAX_NUMBER_OF_PROJECTS}"

        project = Project(id=str(uuid.uuid4()), name=name, description=description)
        self.storage.add_project(project)
        return True, "Project created successfully"

    def find_project(self, index: int) -> Optional[Project]:
        if index>len(self.storage.projects) or index<=0 :
            return None
        return self.storage.projects[index-1]

    def print_all_projects(self) -> List[Project]:
        return self.storage.get_all_projects()

    def edit_project(self, index: int, new_name: Optional[str] = None,new_description: Optional[str] = None) -> Tuple[bool, str]:
        idx = index
        if index>len(self.storage.projects) or index<=0:
            return False, "Project not found"

        project = self.storage.projects[idx]
        if new_name is not None:
            if len(new_name) > MAX_PROJECT_NAME_LENGTH:
                return False, f"Project's name cannot exceed {MAX_PROJECT_NAME_LENGTH} characters"
            project.name = new_name

        if new_description is not None:
            if len(new_description) > MAX_PROJECT_DESCRIPTION_LENGTH:
                return False, f"Project's description cannot exceed {MAX_PROJECT_DESCRIPTION_LENGTH} characters"
            project.description = new_description

        return True, "Project updated successfully"

    def delete_project(self, project_id: str) -> Tuple[bool, str]:
        idx = self.storage.find_project_index(project_id)
        if idx == -1:
            return False, "Project not found"

        del self.storage.projects[idx]
        return True, "Project deleted successfully"

    def create_task(self, index: int, title: str, description: str) -> Tuple[bool, str]:
        project = self.find_project(index)
        if len(title) > MAX_TASK_NAME_LENGTH:
            return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"
        if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"

        project_tasks = self.storage.get_project_tasks(project.id)
        if len(project_tasks) >= MAX_NUMBER_OF_TASKS:
            return False, f"Cannot exceed maximum number of tasks per project: {MAX_NUMBER_OF_TASKS}"

        task = Task(id=str(uuid.uuid4()), project_id=project.id, name=title,
                    description=description)
        self.storage.add_task_to_project(project.id, task)
        return True, "Task created successfully"

    def find_task(self, project: Project, task_title: str) -> Optional[Task]:
        for t in project.tasks:
            if t.name == task_title or t.name == task_title:
                return t
        return None

    def edit_task(self, index: int, task_title: str,new_title: Optional[str] = None,description: Optional[str] = None,status: Optional[str] = None) -> Tuple[bool, str]:

        project = self.find_project(index)
        task = self.find_task(project, task_title)
        if not task:
            return False, "Task not found"

        if new_title is not None:
            if len(new_title) > MAX_TASK_NAME_LENGTH:
                return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"
            task.title = new_title

        if description is not None:
            if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
                return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"
            task.description = description

        if status is not None:
            try:
                task_status = TaskStatus(status)
            except ValueError:
                return False, "Invalid status. Must be one of: todo, doing, done"
            task.status = task_status

        return True, "Task updated successfully"

    def delete_task(self, index: int, task_title: str) -> Tuple[bool, str]:
        project = self.find_project(index)
        task = self.find_task(project, task_title)
        if not task:
            return False, "Task not found"
        success = self.storage.delete_task(task.id)
        return (success, "Task deleted successfully") if success else (False, "Failed to delete task")

    def print_project_tasks(self, index: int) -> list[Task] | None:
        if index>len(self.storage.projects) or index<=0 :
            return None
        project = self.find_project(index)
        if not project:
            return None
        tasks = self.storage.get_project_tasks(project.id)
        return tasks
