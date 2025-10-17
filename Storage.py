from models import Project, Task


class Memory:
    def __init__(self):
        self.projects: list[Project] = []
        self.tasks: list[Task] = []

    def add_project(self, project: Project) -> None:
        self.projects.append(project)
    def edite_project(self, project_id: str, name: str, description: str) -> bool:
        if project_id in self.projects:
            pass
            return True
        return False

    def delete_project(self, project_id: str) -> bool:
        if project_id in self.projects:
            pass
            return True
        return False
    def get_project(self, project_id: str) -> Project:
        pass

