from abc import ABC, abstractmethod
from typing import List, Optional
from app.models.project import Project
from sqlalchemy.orm import Session

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


class SqlAlchemyProjectRepository(ProjectRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all_projects(self) -> List[Project]:
        return self.session.query(Project).order_by(Project.created_time).all()

    def add_project(self, project: Project) -> None:
        self.session.add(project)
        self.session.commit()
        self.session.refresh(project)

    def find_project_index(self, project_id: str) -> int:
        projects = self.get_all_projects()
        for idx, p in enumerate(projects):
            if p.id == project_id:
                return idx
        return -1

    def project_exists(self, name: str) -> bool:
        return self.session.query(Project).filter(Project.name == name).first() is not None

    def get_project(self, project_id: str) -> Optional[Project]:
        return self.session.query(Project).filter(Project.id == project_id).first()

    def delete_project(self, project_id: str) -> bool:
        project = self.get_project(project_id)
        if project:
            self.session.delete(project)  # Cascade delete در مدل هندل می‌شود
            self.session.commit()
            return True
        return False

    def edit_project_name(self, project_id: str, new_name: str) -> bool:
        project = self.get_project(project_id)
        if project:
            project.name = new_name
            self.session.commit()
            return True
        return False

    def edit_project_description(self, project_id: str, new_desc: str) -> bool:
        project = self.get_project(project_id)
        if project:
            project.description = new_desc
            self.session.commit()
            return True
        return False