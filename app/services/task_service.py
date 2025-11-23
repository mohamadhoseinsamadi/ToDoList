import uuid
from datetime import datetime
from typing import Optional, Tuple, List
from app.models.task import Task, TaskStatus
from app.config import (
    MAX_NUMBER_OF_TASKS,
    MAX_TASK_NAME_LENGTH,
    MAX_TASK_DESCRIPTION_LENGTH,
)
from app.repositories.task_repository import TaskRepository


class TaskService:
    def __init__(self, task_repo: TaskRepository):
        self.task_repo = task_repo

    def _parse_status(self, status_input):
        if isinstance(status_input, TaskStatus):
            return status_input

        if status_input is None:
            return TaskStatus.TODO

        if isinstance(status_input, str):
            s = status_input.strip().lower()
            if s == "" or s == "todo":
                return TaskStatus.TODO
            elif s == "doing":
                return TaskStatus.DOING
            elif s == "done":
                return TaskStatus.DONE

        return None

    def create_task(self, project_id: str, title: str, description: str, status=TaskStatus.TODO,
                    deadline: datetime = None) -> Tuple[bool, str]:

        if not title or title.strip() == "":
            return False, "Task name cannot be empty"

        if len(title) > MAX_TASK_NAME_LENGTH:
            return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"
        if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"

        parsed_status = self._parse_status(status)
        if parsed_status is None:
            return False, "Invalid status. Must be {todo, doing, done}."

        tasks = self.task_repo.get_project_tasks(project_id)
        if len(tasks) >= MAX_NUMBER_OF_TASKS:
            return False, f"Cannot exceed max tasks per project: {MAX_NUMBER_OF_TASKS}"

        task = Task(
            id=str(uuid.uuid4()),
            project_id=project_id,
            name=title,
            status=parsed_status,
            description=description,
            deadline=deadline
        )
        self.task_repo.add_task(task)
        return True, "Task created successfully"

    def check_task_exists(self, project_id: str, task_index: id):
        tasks = self.task_repo.get_project_tasks(project_id)
        if task_index < 1 or task_index > len(tasks):
            return None
        return self.task_repo.task_exists(tasks[task_index-1].id)

    def find_task(self, project_id: str, task_index: id) -> Optional[Task]:
        tasks = self.task_repo.get_project_tasks(project_id)

        if task_index < 1 or task_index > len(tasks):
            return None
        return tasks[task_index - 1]

    def edit_task(self, project_id: str, task_index: int, new_title: Optional[str] = None,
                  new_description: Optional[str] = None,
                  status: Optional[str] = None,
                  new_deadline: datetime = None) -> Tuple[bool, str]:

        task = self.find_task(project_id=project_id, task_index=task_index)

        if task is None:
            return False, "Task not found"

        if new_title is not None:
            if new_title.strip() == "":
                return False, "Task name cannot be empty"
            if len(new_title) > MAX_TASK_NAME_LENGTH:
                return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"
            self.task_repo.update_task(project_id=project_id, task_id=task.id, title=new_title)

        if new_description is not None:
            if len(new_description) > MAX_TASK_DESCRIPTION_LENGTH:
                return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"
            self.task_repo.update_task(project_id=project_id, task_id=task.id, description=new_description)

        if status is not None and status.strip() != "":
            parsed_status = self._parse_status(status)
            if parsed_status is None:
                return False, "Invalid status type."
            self.task_repo.update_task(project_id=project_id, task_id=task.id, status=parsed_status)

        if new_deadline is not None:
            self.task_repo.update_task(project_id=project_id, task_id=task.id, deadline=new_deadline)

        return True, "Task updated successfully"

    def delete_task(self, project_id: str, task_index: int) -> Tuple[bool, str]:
        task = self.find_task(project_id, task_index)
        if task is None:
            return False, "Task not found"
        self.task_repo.delete_task(task.id)
        return True, "Task deleted successfully"

    def print_project_tasks(self, project_id: str) -> Optional[List[Task]]:
        tasks = self.task_repo.get_project_tasks(project_id)
        return tasks if tasks else None
