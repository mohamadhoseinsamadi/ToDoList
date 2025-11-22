import uuid
from datetime import datetime
from typing import List, Optional, Tuple
from app.models.task import Task, TaskStatus
from app.config import (
    MAX_NUMBER_OF_PROJECTS,
    MAX_NUMBER_OF_TASKS,
    MAX_PROJECT_NAME_LENGTH,
    MAX_PROJECT_DESCRIPTION_LENGTH,
    MAX_TASK_NAME_LENGTH,
    MAX_TASK_DESCRIPTION_LENGTH,
)
from app.memory.storage import Memory


class TaskService:
    def __init__(self, storage: Memory):
        self.storage = storage

    def check_task_exists(self, project_index: int, task_index: int) -> bool:
        return self.find_task(project_index, task_index) is not None

    def _find_project_by_index(self, index: int):
        projects = self.storage.get_all_projects()
        if index < 1 or index > len(projects):
            return None
        return projects[index - 1]

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

    def create_task(self, index: int, title: str, description: str, status=TaskStatus.TODO,
                    deadline: datetime = None) -> Tuple[bool, str]:
        proj = self._find_project_by_index(index)
        if proj is None:
            return False, "Project not found"

        if not title or title.strip() == "":
            return False, "Task name cannot be empty"

        if len(title) > MAX_TASK_NAME_LENGTH:
            return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"
        if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"

        parsed_status = self._parse_status(status)
        if parsed_status is None:
            return False, "Invalid status. Must be {todo, doing, done}."

        tasks = self.storage.get_project_tasks(proj.id)
        if len(tasks) >= MAX_NUMBER_OF_TASKS:
            return False, f"Cannot exceed max tasks per project: {MAX_NUMBER_OF_TASKS}"

        task = Task(
            id=str(uuid.uuid4()),
            project_id=proj.id,
            name=title,
            status=parsed_status,
            description=description,
            deadline=deadline
        )
        self.storage.add_task_to_project(proj.id, task)
        return True, "Task created successfully"

    def find_task(self, project_index, task_index) -> Optional[Task]:
        proj = self._find_project_by_index(project_index)
        if not proj:
            return None

        tasks = self.storage.get_project_tasks(proj.id)

        if task_index < 1 or task_index > len(tasks):
            return None
        return tasks[task_index - 1]

    def edit_task(self, project_index: int, task_index: int, new_title: Optional[str] = None,
                  new_description: Optional[str] = None,
                  status: Optional[str] = None,
                  new_deadline: datetime = None) -> Tuple[bool, str]:

        proj = self._find_project_by_index(project_index)
        if proj is None:
            return False, "Project not found"

        task = self.find_task(project_index, task_index)
        if task is None:
            return False, "Task not found"

        if new_title is not None:
            if new_title.strip() == "":
                return False, "Task name cannot be empty"
            if len(new_title) > MAX_TASK_NAME_LENGTH:
                return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"
            self.storage.update_task(proj.id, task.id, title=new_title)

        if new_description is not None:
            if len(new_description) > MAX_TASK_DESCRIPTION_LENGTH:
                return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"
            self.storage.update_task(proj.id, task.id, description=new_description)

        if status is not None and status.strip() != "":
            parsed_status = self._parse_status(status)
            if parsed_status is None:
                return False, "Invalid status type."
            self.storage.update_task(proj.id, task.id, status=parsed_status)

        if new_deadline is not None:
            self.storage.update_task(proj.id, task.id, deadline=new_deadline)

        return True, "Task updated successfully"

    def delete_task(self, project_index: int, task_index: int) -> Tuple[bool, str]:
        task = self.find_task(project_index, task_index)
        if task is None:
            return False, "Task not found"
        success = self.storage.delete_task(task.id)
        return (True, "Task deleted successfully") if success else (False, "Failed to delete Task")
