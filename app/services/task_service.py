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

    def create_task(self, index: int, title: str, description: str, status=TaskStatus.TODO,
                    deadline: datetime = None) -> Tuple[bool, str]:
        proj = self.find_project(index)
        if proj is None:
            return False, "Project not found"
        if len(title) > MAX_TASK_NAME_LENGTH:
            return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"
        if len(description) > MAX_TASK_DESCRIPTION_LENGTH:
            return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"
        if status == "todo" or "":
            status = TaskStatus.TODO
        elif status == "doing":
            status = TaskStatus.DOING
        elif status == "done":
            status = TaskStatus.DONE
        if not isinstance(status, TaskStatus):
            return False, "Invalid status. Must be {todo,doing,done}."
        tasks = self.storage.get_project_tasks(proj.id)
        if len(tasks) >= MAX_NUMBER_OF_TASKS:
            return False, f"Cannot exceed max tasks per project: {MAX_NUMBER_OF_TASKS}"

        task = Task(
            id=str(uuid.uuid4()),
            project_id=proj.id,
            name=title,
            status=status,
            description=description
        )
        self.storage.add_task_to_project(proj.id, task)
        return True, "Task created successfully"


    def find_task(self, project_index, task_index) -> Optional[Task]:
        project = self.find_project(project_index)
        if task_index < 1 or task_index > len(self.storage.get_project_tasks(project.id)):
            return None
        return project.tasks[task_index - 1]


    def edit_task(self, project_index: int, task_index: int, new_title: Optional[str] = None,
                  new_description: Optional[str] = None,
                  status=TaskStatus.TODO, new_deadline: datetime = None) -> Tuple[bool, str]:
        proj = self.find_project(project_index)
        if proj is None:
            return False, "Project not found"

        task = self.find_task(project_index, task_index)
        if task is None:
            return False, "Task not found"
        if new_title is not None:
            if len(new_title) > MAX_TASK_NAME_LENGTH:
                return False, f"Task title cannot exceed {MAX_TASK_NAME_LENGTH} characters"
            self.storage.update_task(proj.id, task.id, title=new_title)

        if new_description is not None:
            if len(new_description) > MAX_TASK_DESCRIPTION_LENGTH:
                return False, f"Task description cannot exceed {MAX_TASK_DESCRIPTION_LENGTH} characters"
            self.storage.update_task(proj.id, task.id, description=new_description)

        if status == "todo" or "":
            status = TaskStatus.TODO
        elif status == "doing":
            status = TaskStatus.DOING
        elif status == "done":
            status = TaskStatus.DONE
        self.storage.update_task(proj.id, task.id, status=status)

        return True, "Task updated successfully"


    def delete_task(self, project_index: int, task_index: int) -> Tuple[bool, str]:
        task = self.find_task(project_index, task_index)
        if task is None:
            return False, "Task not found"
        success = self.storage.delete_task(task.id)
        return (True, "Task deleted successfully") if success else (False, "Failed to delete Task")
