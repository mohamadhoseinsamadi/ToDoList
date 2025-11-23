from datetime import datetime
from app.services.project_service import ProjectService
from app.services.task_service import TaskService


class ToDoManager:
    def __init__(self, project_service: ProjectService, task_service: TaskService):
        self.project_service = project_service
        self.task_service = task_service

    def _get_input(self, prompt: str, required=True) -> str | None:
        value = input(prompt).strip()
        if required and not value:
            print("Error: This field is required.")
            return None
        return value if value else None

    def _get_int(self, prompt: str) -> int | None:
        value = input(prompt).strip()
        try:
            return int(value)
        except ValueError:
            print("Error: Please enter a valid number.")
            return None

    def _get_date(self, prompt: str) -> datetime | None:
        value = input(prompt).strip()
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            print("Error: Invalid date format. Use YYYY-MM-DD.")
            return None

    def print_projects(self) -> bool:
        projs = self.project_service.print_all_projects()
        if not projs:
            print("No projects found.\n")
            return False
        print("\n#### Projects ####")
        for i, p in enumerate(projs, start=1):
            print(f"{i}. {p.name} (Created: {p.created_time.strftime('%Y-%m-%d')})")
            if p.description:
                print(f"   Desc: {p.description}")
        print("-" * 20 + "\n")
        return True

    def view_project_details(self, index: int):
        proj = self.project_service.find_project(index)
        if not proj:
            print("Project not found.\n")
            return

        print(f"\n=== Project Details ===")
        print(f"Name: {proj.name}")
        print(f"Description: {proj.description}")
        print(f"Created At: {proj.created_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("=======================\n")

    def list_project_tasks(self, project_index: int) -> bool:
        proj = self.project_service.find_project(index=project_index)
        if proj is None:
            print("Project not found.\n")
            return False
        tasks = self.task_service.print_project_tasks(project_id=proj.id)
        if not tasks:
            print("No tasks in this project.\n")
            return False

        print(f"\n#### Tasks for Project {project_index} ####")
        for i, t in enumerate(tasks, start=1):
            deadline_str = t.deadline.strftime('%Y-%m-%d') if t.deadline else "No Deadline"
            print(f"{i}. {t.name} ({t.status.value}) - Due: {deadline_str}")
        print("-" * 20 + "\n")
        return True

    def view_task_details(self, project_index: int, task_index: int):
        proj = self.project_service.find_project(index=project_index)
        task = self.task_service.find_task(project_id=proj.id, task_index=task_index)
        if not task:
            print("Task not found.\n")
            return

        print(f"\n--- Task Details ---")
        print(f"Title:       {task.name}")
        print(f"Status:      {task.status.value}")
        print(f"Description: {task.description}")
        deadline_str = task.deadline.strftime('%Y-%m-%d') if task.deadline else "None"
        print(f"Deadline:    {deadline_str}")
        print(f"Created:     {task.created_time.strftime('%Y-%m-%d %H:%M')}")
        print("--------------------\n")

    def handle_add_project(self):
        name = self._get_input("Enter project name: ")
        if not name:
            return
        desc = input("Enter description (optional): ").strip()
        ok, msg = self.project_service.add_project(name, desc)
        print(f">> {msg}\n")

    def handle_edit_project(self, index: int):
        new_name = input("New name (Press Enter to skip): ").strip() or None
        new_desc = input("New description (Press Enter to skip): ").strip() or None

        if new_name is None and new_desc is None:
            print("No changes made.")
            return

        ok, msg = self.project_service.edit_project(index, new_name, new_desc)
        print(f">> {msg}\n")

    def handle_add_task(self, project_index: int):
        title = self._get_input("Enter task title: ")
        if not title: return
        desc = input("Enter description (optional): ").strip()

        deadline = self._get_date("Enter deadline (YYYY-MM-DD) or skip: ")

        status_str = input("Status (todo/doing/done): ").strip()

        proj = self.project_service.find_project(project_index)

        ok, msg = self.task_service.create_task(proj.id, title, desc, status=status_str, deadline=deadline)
        print(f">> {msg}\n")

    def handle_edit_task(self, project_index: int, task_index: int):
        proj = self.project_service.find_project(index=project_index)
        print("Leave fields empty to keep current values.")
        new_title = input("New title: ").strip() or None
        new_desc = input("New description: ").strip() or None
        new_status = input("New status (todo/doing/done): ").strip() or None
        new_deadline = self._get_date("New deadline (YYYY-MM-DD): ")

        ok, msg = self.task_service.edit_task(
            project_id=proj.id, task_index=task_index,
            new_title=new_title,
            new_description=new_desc,
            status=new_status,
            new_deadline=new_deadline
        )
        print(f">> {msg}\n")

    def delete_task(self, project_index: int, task_index: int):
        proj = self.project_service.find_project(index=project_index)
        ok, msg = self.task_service.delete_task(project_id=proj.id, task_index=task_index)
        print(f">> {msg}\n")
