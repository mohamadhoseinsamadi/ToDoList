import uuid
from datetime import datetime
from typing import Optional, Tuple, List

from app.api.controller_schemas.requests.task_request_schema import TaskUpdateRequest
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
                    deadline: datetime = None) -> Tuple[bool, str, Optional[Task]]:

        if not title or title.strip() == "":
            return False, "Task name cannot be empty", None

        if len(title) > MAX_TASK_NAME_LENGTH:
            return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters", None
        if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters", None

        parsed_status = self._parse_status(status)
        if parsed_status is None:
            return False, "Invalid status. Must be {todo, doing, done}.", None

        tasks = self.task_repo.get_project_tasks(project_id)
        if len(tasks) >= MAX_NUMBER_OF_TASKS:
            return False, f"Cannot exceed max tasks per project: {MAX_NUMBER_OF_TASKS}", None

        task = Task(
            id=str(uuid.uuid4()),
            project_id=project_id,
            name=title,
            status=parsed_status,
            description=description,
            deadline=deadline
        )
        self.task_repo.add_task(task)
        return True, "Task created successfully", task

    def check_task_exists(self, project_id: str, task_index: id):
        tasks = self.task_repo.get_project_tasks(project_id)
        if task_index < 1 or task_index > len(tasks):
            return None
        return self.task_repo.task_exists(tasks[task_index - 1].id)

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

    def autoclose_overdue_tasks(self) -> None:
        time = datetime.now()
        self.task_repo.autoclose_overdue_tasks(time)

    def find_task_by_id(self, project_id: str, task_id: str) -> Optional[Task]:
        """Find task by ID ensuring it belongs to the project"""
        task = self.task_repo.get_task_by_id(task_id=task_id, project_id=project_id)
        return task

    def find_task_byid(self, task_id: str) -> Optional[Task]:
        """Find a task by its global ID."""
        return self.task_repo.get_task(task_id)

    def edit_task_by_id(self, project_id: str, task_id: str, new_title: Optional[str] = None,
                        new_description: Optional[str] = None,
                        status: Optional[str] = None,
                        new_deadline: datetime = None) -> Tuple[bool, str]:

        task = self.find_task_by_id(project_id, task_id)
        if task is None:
            return False, "Task not found"

        if new_title is not None:
            if new_title.strip() == "":
                return False, "Task name cannot be empty"
            if len(new_title) > MAX_TASK_NAME_LENGTH:
                return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"

        if new_description is not None:
            if len(new_description) > MAX_TASK_DESCRIPTION_LENGTH:
                return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"

        parsed_status = None
        if status is not None:
            parsed_status = self._parse_status(status)
            if parsed_status is None and status != "":
                return False, "Invalid status type."

        self.task_repo.update_task(
            project_id=project_id,
            task_id=task_id,
            title=new_title,
            description=new_description,
            status=parsed_status,
            deadline=new_deadline
        )
        return True, "Task updated successfully"

    def delete_task_by_id(self, project_id: str, task_id: str) -> Tuple[bool, str]:
        task = self.find_task_by_id(project_id, task_id)
        if task is None:
            return False, "Task not found"
        self.task_repo.delete_task(task.id)
        return True, "Task deleted successfully"

    def print_all_tasks(self) -> Optional[List[Task]]:
        """
        Retrieves all tasks in the system.
        """
        return self.task_repo.get_all_tasks()

    def update_task_by_id(self, task_id: str, request_data: TaskUpdateRequest) -> Tuple[bool, str]:
        """Update a task globally by its ID."""

        task = self.find_task_byid(task_id)
        if not task:
            return False, "Task not found"

        if request_data.name is not None and not request_data.name.strip():
            return False, "Task name cannot be empty"

        update_args = {}
        if request_data.name is not None:
            update_args['title'] = request_data.name
        if request_data.description is not None:
            update_args['description'] = request_data.description
        if request_data.status is not None:
            update_args['status'] = request_data.status
        if request_data.deadline is not None:
            update_args['deadline'] = request_data.deadline

        if not update_args:
            return True, "No fields provided to update"

        success = self.task_repo.update_task_global(task_id, **update_args)

        if success:
            return True, "Task updated successfully"
        else:
            return False, "Could not update task in repository"

    def delete_task_by_id_global(self, task_id: str) -> Tuple[bool, str]:
        """Delete a task globally by its ID."""
        task = self.find_task_byid(task_id)
        if not task:
            return False, "Task not found"

        success = self.task_repo.delete_task(task_id)

        if success:
            return True, "Task deleted successfully"
        else:
            return False, "Could not delete task"
