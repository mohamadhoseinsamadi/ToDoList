from datetime import datetime
from enum import Enum
from typing import Optional, List


class Project:
    def __init__(self, id, name, description=""):
        self.id = id
        self.name = name
        self.description = description
        self.tasks: List[Task] = []
        self.created_time = datetime.now()


class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class Task:
    def __init__(self, id: str, project_id: str, name: str, description: str = "",status:TaskStatus=TaskStatus.TODO):
        self.id = id
        self.project_id = project_id
        self.name = name
        self.description = description
        self.status = status
        self.created_time = datetime.now()
        deadline: Optional[datetime] = None

