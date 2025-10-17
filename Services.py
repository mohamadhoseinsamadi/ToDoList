import uuid

from models import Project
from config import (
    MAX_NUMBER_OF_PROJECTS,
    MAX_TASKS,
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
            print(f"Project name cannot exceed {MAX_PROJECT_NAME_LENGTH} characters")
        elif len(description) > MAX_PROJECT_DESCRIPTION_LENGTH:
            print(f"Project description cannot exceed {MAX_PROJECT_DESCRIPTION_LENGTH} characters")
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
