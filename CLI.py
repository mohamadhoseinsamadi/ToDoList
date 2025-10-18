from Storage import Memory
from Services import ProjectTaskService
from models import Project, Task, TaskStatus

class ToDoManager:
    def __init__(self):
        self.storage = Memory()
        self.project_service = ProjectTaskService(self.storage)

    def create_project(self, name: str, description: str):
        state, message = self.project_service.add_project(name, description)
        print(message, "", sep="\n")

    def view_project(self,index):
        project=self.project_service.find_project(index)
        if project:
            print(index, "_")
            print(f"Name: {project.name}")
            if project.description:
                print(f"Description: {project.description}")
            print(f"Created: {project.created_time}")
            print("____________________")
            print()

    def edit_project(self, index: int, new_name: str, description: str):
        state, message = self.project_service.edit_project(index, new_name, description)
        print(message, "", sep="\n")

    def print_projects(self)->bool:
        projects = self.project_service.print_all_projects()
        if not projects:
            print("No projects found\n")
            return False
        else:
            print("\n#### Projects ####\n")
            i:int
            i=1
            for project in projects:
                print(i,"_")
                print(f"Name: {project.name}")
                if project.description:
                    print(f"Description: {project.description}")
                print(f"Created: {project.created_time}")
                print("____________________")
                print()
                i=i+1
            return True

    def create_task(self, index: int, title: str, description: str):
        state, message = self.project_service.create_task(index, title, description)
        print(message)

    def edit_task(self, index: int, task_title: str, new_title: str, description: str, status: str):
        ok, message = self.project_service.edit_task(index, task_title, new_title, description, status)
        print(message)

    def delete_task(self, index: int, task_title: str):
        ok, message = self.project_service.delete_task(index, task_title)
        print(message)

    def list_project_tasks(self, index: int):
        tasks = self.project_service.print_project_tasks(index)
        if not tasks:
            print("No tasks found for this project.")
            return
        print(f"\n#### Tasks for project: {index} ####")
        for t in tasks:
            print(f"Title: {t.name} ")
            if t.description:
                print(f"Description: {t.description}")
            print(f"Status: {t.status}")
            print(f"Created: {t.created_time}")
            print("--------------")
            print()

    def find_project_by_name(self, index: int):
        proj = self.project_service.find_project(index)
        if proj:
            print(f"Found project: {proj.name} (ID: {proj.id})")
        else:
            print("Project not found")
