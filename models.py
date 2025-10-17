from datetime import datetime
from enum import Enum
from typing import Optional


class Project:
    def __init__(self, id, name, description=""):
        self.id = id
        self.name = name
        self.description = description
        self.tasks = []
        self.created_time = datetime.now()

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]


class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class Task:
    def __init__(self, id: str, project_id: str, name: str, description: str = ""):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.status = TaskStatus.TODO
        deadline: Optional[datetime] = None

