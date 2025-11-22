from datetime import datetime
from typing import List
from app.models.task import Task
class Project:
    def __init__(self, id: str, name: str, description: str = ""):
        self.id = id
        self.name = name
        self.description = description
        self.tasks: List[Task] = []
        self.created_time = datetime.now()
