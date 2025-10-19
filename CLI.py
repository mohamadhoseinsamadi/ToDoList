from datetime import datetime

from Storage import Memory
from Services import ProjectTaskService
from models import Project, Task, TaskStatus


class ToDoManager:
    def __init__(self):
        self.storage = Memory()
        self.project_service = ProjectTaskService(self.storage)

    def create_project(self, name: str, description: str = ""):
        ok, msg = self.project_service.add_project(name, description)
        print(msg, end="\n\n")

    def print_projects(self) -> bool:
        projs = self.project_service.print_all_projects()
        if not projs:
            print("No projects found\n")
            return False
        print("#### Projects ####\n")
        for i, p in enumerate(projs, start=1):
            print(f"{i}. {p.name}")
            if p.description:
                print(f"   Description: {p.description}")
            print(f"   Created: {p.created_time}\n")
        return True

    def view_project(self, index: int):
        proj = self.project_service.find_project(index)
        if not proj:
            print("Project not found\n")
            return
        print(f"{index}. {proj.name}")
        if proj.description:
            print(f"   Description: {proj.description}")
        print(f"   Created: {proj.created_time}\n")

    def edit_project(self, index: int, new_name: str = None, new_description: str = None):
        ok, msg = self.project_service.edit_project(index, new_name, new_description)
        print(msg, end="\n\n")

    def delete_project(self, index: int):
        ok, msg = self.project_service.delete_project(index)
        print(msg, end="\n\n")

    def create_task(self, index: int, title: str, description: str = "", status=TaskStatus.TODO,
                    deadline: datetime = None):
        ok, msg = self.project_service.create_task(index, title, description, status)
        print(msg, end="\n\n")

    def list_project_tasks(self, index: int)->bool:
        tasks = self.project_service.print_project_tasks(index)
        if tasks is None:
            print("Project not found\n")
            return False
        if not tasks:
            print("No tasks found\n")
            return False
        print(f"#### Tasks for project {index} ####\n")
        for t in tasks:
            print(f"- {t.name} (Status: {t.status}, Created: {t.created_time})")
            if t.description:
                print(f"   Description: {t.description}")
            print()
        return True
    def view_task(self,project_index:int ,task_index:int)->bool:
        tasks = self.project_service.print_project_tasks(project_index)
        if not tasks:
            print("No tasks found\n")
            return False
        t=tasks[task_index]
        print(f"- {t.name} (Status: {t.status}, Created: {t.created_time})")
        if t.description:
            print(f"   Description: {t.description}")
        print()
        return True