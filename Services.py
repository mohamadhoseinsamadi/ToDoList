import uuid
from datetime import datetime
from typing import List, Optional, Tuple
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

    def is_exist_project_by_name(self, name: str)->bool:
        for project in self.storage.projects:
            if project.name == name:
                return True
        return False

    def add_project(self, name: str, description: str) -> Tuple[bool, str]:
        if name == "":
            return False, "name can not be empty"
        if self.is_exist_project_by_name(name):
            return False, "name can not be same as other projects"
        if len(name) > MAX_PROJECT_NAME_LENGTH:
            return False, f"Project's name cannot exceed {MAX_PROJECT_NAME_LENGTH} characters"
        if len(description) > MAX_PROJECT_DESCRIPTION_LENGTH:
            return False, f"Project's description cannot exceed {MAX_PROJECT_DESCRIPTION_LENGTH} characters"
        if len(self.storage.get_all_projects()) >= MAX_NUMBER_OF_PROJECTS:
            return False, f"Cannot exceed maximum number of projects: {MAX_NUMBER_OF_PROJECTS}"

        proj = Project(id=str(uuid.uuid4()), name=name, description=description)
        self.storage.add_project(proj)
        return True, "Project created successfully"

    def find_project(self, index: int) -> Optional[Project]:
        projects = self.storage.get_all_projects()
        if index < 1 or index > len(projects):
            return None
        return projects[index - 1]

    def print_all_projects(self) -> List[Project]:
        return self.storage.get_all_projects()

    def edit_project(
            self,
            index: int,
            new_name: Optional[str] = None,
            new_description: Optional[str] = None
    ) -> Tuple[bool, str]:
        proj = self.find_project(index)
        if proj is None:
            return False, "Project not found"
        if new_name is not None:
            if len(new_name) > MAX_PROJECT_NAME_LENGTH:
                return False, f"Project's name cannot exceed {MAX_PROJECT_NAME_LENGTH} characters"
        if new_name == "":
            return False, "name can not be empty"
        if self.is_exist_project_by_name(new_name):
            return False, "name can not be same as other projects"
        self.storage.edit_project_name(proj.id, new_name)
        if new_description is not None:
            if len(new_description) > MAX_PROJECT_DESCRIPTION_LENGTH:
                return False, f"Project's description cannot exceed {MAX_PROJECT_DESCRIPTION_LENGTH} characters"
            self.storage.edit_project_description(proj.id, new_description)

        return True, "Project updated successfully"

    def delete_project(self, index: int) -> Tuple[bool, str]:
        proj = self.find_project(index)
        if proj is None:
            return False, "Project not found"
        success = self.storage.delete_project(proj.id)
        return (True, "Project deleted successfully") if success else (False, "Failed to delete project")

    def create_task(self, index: int, title: str, description: str,status=TaskStatus.TODO,deadline:datetime=None) -> Tuple[bool, str]:
        proj = self.find_project(index)
        if proj is None:
            return False, "Project not found"
        if len(title) > MAX_TASK_NAME_LENGTH:
            return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"
        if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"
        if status=="todo":
            status=TaskStatus.TODO
        elif status=="doing":
            status=TaskStatus.DOING
        elif status=="done":
            status=TaskStatus.DONE
        if not isinstance(status, TaskStatus):
            return False, "Invalid status. Must be {todo,doing,done}."
        tasks = self.storage.get_project_tasks(proj.id)
        if len(tasks) >= MAX_NUMBER_OF_TASKS:
            return False, f"Cannot exceed max tasks per project: {MAX_NUMBER_OF_TASKS}"

        task = Task(
            id=str(uuid.uuid4()),
            project_id=proj.id,
            name=title,
            status=status,
            description=description
        )
        self.storage.add_task_to_project(proj.id, task)
        return True, "Task created successfully"

    def find_task(self, proj: Project, identifier: str) -> Optional[Task]:
        for t in proj.tasks:
            if t.id == identifier or t.name == identifier:
                return t
        return None

    def edit_task(
            self,
            index: int,
            identifier: str,
            new_title: Optional[str] = None,
            new_description: Optional[str] = None,
            status: Optional[str] = None
    ) -> Tuple[bool, str]:
        proj = self.find_project(index)
        if proj is None:
            return False, "Project not found"

        task = self.find_task(proj, identifier)
        if task is None:
            return False, "Task not found"

        if new_title is not None:
            if len(new_title) > MAX_TASK_NAME_LENGTH:
                return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"
            self.storage.update_task(proj.id, task.id, title=new_title)

        if new_description is not None:
            if len(new_description) > MAX_TASK_DESCRIPTION_LENGTH:
                return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"
            self.storage.update_task(proj.id, task.id, description=new_description)

        if status is not None:
            try:
                TaskStatus(status)
            except ValueError:
                return False, "Invalid status. Must be one of: todo, doing, done"
            self.storage.update_task(proj.id, task.id, status=status)

        return True, "Task updated successfully"

    def delete_task(self, index: int, identifier: str) -> Tuple[bool, str]:
        proj = self.find_project(index)
        if proj is None:
            return False, "Project not found"

        task = self.find_task(proj, identifier)
        if task is None:
            return False, "Task not found"

        success = self.storage.delete_task(task.id)
        return (True, "Task deleted successfully") if success else (False, "Failed to delete task")

    def print_project_tasks(self, index: int) -> Optional[List[Task]]:
        proj = self.find_project(index)
        return self.storage.get_project_tasks(proj.id) if proj else None
