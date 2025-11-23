from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.project import Project


class ProjectRepository(ABC):

    @abstractmethod
    def find_project_index(self, project_id: str) -> int:
        pass

    @abstractmethod
    def add_project(self, project: Project) -> None:
        pass

    @abstractmethod
    def edit_project_name(self, project_id: str, new_name: str) -> bool:
        pass

    @abstractmethod
    def edit_project_description(self, project_id: str, new_desc: str) -> bool:
        pass

    @abstractmethod
    def delete_project(self, project_id: str) -> bool:
        pass

    @abstractmethod
    def get_project(self, project_id: str) -> Optional[Project]:
        pass

    @abstractmethod
    def get_all_projects(self) -> List[Project]:
        pass

    @abstractmethod
    def project_exists(self, name: str) -> bool:
        pass


class InMemoryProjectRepository(ProjectRepository):
    def __init__(self):
        self.projects: List[Project] = []

    def find_project_index(self, project_id: str) -> int:
        for idx, project in enumerate(self.projects):
            if project.id == project_id:
                return idx
        return -1

    def add_project(self, project: Project) -> None:
        self.projects.append(project)

    def edit_project_name(self, project_id: str, new_name: str) -> bool:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return False
        self.projects[idx].name = new_name
        return True

    def edit_project_description(self, project_id: str, new_desc: str) -> bool:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return False
        self.projects[idx].description = new_desc
        return True

    def delete_project(self, project_id: str) -> bool:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return False
        self.projects[idx].tasks.clear()
        self.projects.pop(idx)

        return True

    def get_project(self, project_id: str) -> Optional[Project]:
        idx = self.find_project_index(project_id)
        if idx == -1:
            return None
        return self.projects[idx]

    def get_all_projects(self) -> List[Project]:
        return self.projects

    def project_exists(self, name: str) -> bool:
        return any(p.name.lower() == name.lower() for p in self.projects)
