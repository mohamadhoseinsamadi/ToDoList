import uuid

from models import Project
from config import (
    MAX_NUMBER_OF_PROJECTS,
    MAX_NUMBER_OF_TASKS,
    MAX_PROJECT_NAME_LENGTH,
    MAX_PROJECT_DESCRIPTION_LENGTH,
    MAX_TASK_NAME_LENGTH,
    MAX_TASK_DESCRIPTION_LENGTH
)
from Storage import Memory


class ProjectService:
    def __init__(self, storage: Memory):
        self.storage = storage

    def add_project(self, name: str, description: str):
        if len(name) > MAX_PROJECT_NAME_LENGTH:
            print(f"Project's name cannot exceed {MAX_PROJECT_NAME_LENGTH} characters")
        elif len(description) > MAX_PROJECT_DESCRIPTION_LENGTH:
            print(f"Project's description cannot exceed {MAX_PROJECT_DESCRIPTION_LENGTH} characters")
        elif len(self.storage.projects) >= MAX_NUMBER_OF_PROJECTS:
            print(f"Cannot exceed maximum number of projects: {MAX_NUMBER_OF_PROJECTS}")
        else:
            project = Project(id=str(uuid.uuid4()), name=name, description=description)
            self.storage.add_project(project)
            print("Project created successfully")

    def find_project(self, name: str):
        for project in self.storage.projects:
            if project.name == name:
                return project
        return None

    def print_all_projects(self):
        pass

    def edit_project(self):
        pass

    def delete_project(self):
        pass


class TaskService:
    def __init__(self, storage: Memory):
        self.storage = storage
        self.project_service = ProjectService(storage)

    def find_task(self, project_name: str, task_title: str):
        project = self.project_service.find_project(project_name)
        if not project:
            print("Task not found")
        else:
            pass

    def create_task(self, project_name: str, title: str, description: str) -> tuple[bool, str]:
        project = self.project_service.find_project(project_name)
        if not project:
            print("Project not found")
        elif len(title) > MAX_TASK_NAME_LENGTH:
            print(f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters")
        elif len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            print(f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters")
        else:
            project_tasks = self.storage.get_project_tasks(project.id)
            if len(project_tasks) >= MAX_NUMBER_OF_TASKS:
                print( f"Cannot exceed maximum number of tasks per project: {MAX_NUMBER_OF_TASKS}")

        task = Task( id=str(uuid.uuid4()),project_id=project.id,title=title,description=description,status=TaskStatus.TODO)
        self.storage.add_task(task)
        print("Task created successfully")

    def edit_task(self, project_name: str, task_title: str, new_title: str, description: str, status: str) -> tuple[
        bool, str]:
        task = self.find_task(project_name, task_title)
        if not task:
            return False, "Task not found"
        if len(new_title) > MAX_TASK_DESCRIPTION_LENGTH:
            return False, f"Task title cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"

        if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"

        try:
            task_status = TaskStatus(status)
        except ValueError:
            return False, "Invalid status. Must be one of: todo, doing, done"

        success = self.storage.update_task(task.id, new_title, description, task_status)
        return success, "Task updated successfully" if success else "Failed to update task"

    def delete_task(self, project_name: str, task_title: str) -> tuple[bool, str]:
        task = self.get_task_by_title(project_name, task_title)
        if not task:
            return False, "Task not found"

        success = self.storage.delete_task(task.id)
        return success, "Task deleted successfully" if success else "Task not found"

    def list_project_tasks(self, project_name: str) -> tuple[bool, str | List[Task]]:
        project = self.project_service.get_project_by_name(project_name)

        if not project:
            return False, "Project not found"

        tasks = self.storage.get_project_tasks(project.id)
        return True, tasks