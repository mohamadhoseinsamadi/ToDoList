from datetime import datetime

from app.memory.storage import Memory
from app.services.project_service import ProjectService
from app.services.task_service import TaskService
from app.models.task import Task, TaskStatus



class ToDoManager:
    def __init__(self):
        self.storage = Memory()
        self.project_service = ProjectService(self.storage)
        self.task_service = TaskService(self.storage)

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
            print(i, "_",sep="")
            print(f"Name: {p.name}")
            if p.description:
                print(f"Description: {p.description}")
            print(f"Created: {p.created_time}")
            print("____________________")
            print()
        return True

    def view_project(self, index: int):
        proj = self.project_service.find_project(index)
        if not proj:
            print("Project not found\n")
            return
        print(f"project_{index}: {proj.name}")
        if proj.description:
            print(f"   Description: {proj.description}")
        print(f"   Created at: {proj.created_time.year}/{proj.created_time.month}/{proj.created_time.day} "
              f"{proj.created_time.hour}:{proj.created_time.minute}:{proj.created_time.second}\n")

    def edit_project(self, index: int, new_name: str = None, new_description: str = None):
        state, message = self.project_service.edit_project(index, new_name, new_description)
        print(message, "", sep="\n")

    def delete_project(self, index: int):
        ok, msg = self.project_service.delete_project(index)
        print(msg, end="\n\n")

    def create_task(self, index: int, title: str, description: str = "", status=TaskStatus.TODO,
                    deadline: datetime = None):
        ok, msg = self.task_service.create_task(index, title, description, status)
        print(msg, end="\n\n")

    def list_project_tasks(self, index: int) -> bool:
        tasks = self.project_service.print_project_tasks(index)
        if tasks is None:
            print("Project not found\n")
            return False
        if not tasks:
            print("No tasks found\n")
            return False
        print(f"#### Tasks for project {index} ####\n")
        for i, t in enumerate(tasks, start=1):
            print(f"task_{i}: {t.name} ")
            print(f"   Status: {t.status}")
            print(f"   Created at: {t.created_time.year}/{t.created_time.month}/{t.created_time.day} "
                  f"{t.created_time.hour}:{t.created_time.minute}:{t.created_time.second}")
            if t.description:
                print(f"   Description: {t.description}")
            print()
        return True

    def view_task(self, project_index: int, task_index: int) -> bool:
        tasks = self.project_service.print_project_tasks(project_index)
        if not tasks:
            print("No tasks found\n")
            return False
        t = tasks[task_index-1]
        print(f"task_{task_index}: {t.name} ")
        print(f"   Status: {t.status}")
        print(f"   Created at: {t.created_time.year}/{t.created_time.month}/{t.created_time.day} "
              f"{t.created_time.hour}:{t.created_time.minute}:{t.created_time.second}")
        if t.description:
            print(f"   Description: {t.description}")
        print()
        return True

    def delete_task(self, project_index: int, task_index: int):
        ok, msg = self.task_service.delete_task(project_index,task_index)
        print(msg, end="\n\n")

    def edit_task(self, project_index: int, task_index: int, new_name, new_description,new_status,new_deadline):
        state, message = self.task_service.edit_task(project_index,task_index, new_name, new_description,new_status,new_deadline)
        print(message, "", sep="\n")