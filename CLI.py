from models import Project
from config import (
    MAX_NUMBER_OF_PROJECTS,
    MAX_NUMBER_OF_TASKS,
    MAX_PROJECT_NAME_LENGTH,
    MAX_PROJECT_DESCRIPTION_LENGTH,
    MAX_TASK_NAME_LENGTH,
    MAX_TASK_DESCRIPTION_LENGTH
)

class ToDoManager:
    def __init__(self):
        self.projects = []
        self.next_proj_id = 1

    def add_project(self):
        pass

    def edit_project(self):
        pass

    def print_projects(self):
        pass

    def create_project(self, name, description):
        proj = Project(self.next_proj_id, name, description)
        self.projects.append(proj)
        self.next_proj_id += 1

    def find_project(self, proj_id):
        for p in self.projects:
            if p.id == proj_id:
                return p
        raise KeyError("پروژه یافت نشد")
