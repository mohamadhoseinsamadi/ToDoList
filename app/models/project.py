from datetime import datetime
from typing import List

class Project:
    def __init__(self, id, name, description=""):
        self.id = id
        self.name = name
        self.description = description
        self.tasks: List[Task] = []
        self.created_time = datetime.now()
