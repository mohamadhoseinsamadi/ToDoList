import uuid
from typing import List, Optional, Tuple
from app.models.project import Project
from app.models.task import Task
from app.config import (
    MAX_NUMBER_OF_PROJECTS,
    MAX_PROJECT_NAME_LENGTH,
    MAX_PROJECT_DESCRIPTION_LENGTH,
)
from app.repositories.project_repository import ProjectRepository

class ProjectService:
    def __init__(self, repo: ProjectRepository):
        self.repo = repo

    def check_project_exists(self, index: int) -> bool:
        return self.find_project(index) is not None

    def _find_project_by_index(self, index: int) -> Optional[Project]:
        projects = self.repo.get_all_projects()
        if index < 1 or index > len(projects):
            return None
        return projects[index - 1]

    def add_project(self, name: str, description: str) -> Tuple[bool, str]:
        if not name or name.strip() == "":
            return False, "Project name cannot be empty"

        if len(name) > MAX_PROJECT_NAME_LENGTH:
            return False, f"Project name cannot exceed {MAX_PROJECT_NAME_LENGTH} characters"

        if len(description) > MAX_PROJECT_DESCRIPTION_LENGTH:
            return False, f"Project description cannot exceed {MAX_PROJECT_DESCRIPTION_LENGTH} characters"

        if self.repo.project_exists(name):
            return False, "Project name already exists"

        current_count = len(self.repo.get_all_projects())
        if current_count >= MAX_NUMBER_OF_PROJECTS:
            return False, f"Cannot exceed maximum number of projects: {MAX_NUMBER_OF_PROJECTS}"

        proj = Project(id=str(uuid.uuid4()), name=name, description=description)
        self.repo.add_project(proj)
        return True, "Project created successfully"

    def print_all_projects(self) -> List[Project]:
        return self.repo.get_all_projects()

    def find_project(self, index: int) -> Optional[Project]:
        return self._find_project_by_index(index)

    def edit_project(self, index: int, new_name: Optional[str] = None, new_description: Optional[str] = None) -> Tuple[
        bool, str]:
        proj = self._find_project_by_index(index)
        if proj is None:
            return False, "Project not found"

        if new_name is not None:
            s_name = new_name.strip()
            if s_name == "":
                return False, "Project name cannot be empty"
            if len(s_name) > MAX_PROJECT_NAME_LENGTH:
                return False, f"Name exceeds max length ({MAX_PROJECT_NAME_LENGTH})"

            if s_name != proj.name and self.repo.project_exists(s_name):
                return False, "Project name already exists"

            self.repo.edit_project_name(proj.id, s_name)

        if new_description is not None:
            if len(new_description) > MAX_PROJECT_DESCRIPTION_LENGTH:
                return False, f"Description exceeds max length ({MAX_PROJECT_DESCRIPTION_LENGTH})"
            self.repo.edit_project_description(proj.id, new_description)

        return True, "Project updated successfully"

    def delete_project(self, index: int) -> Tuple[bool, str]:
        proj = self._find_project_by_index(index)
        if proj is None:
            return False, "Project not found"

        success = self.repo.delete_project(proj.id)
        return (True, "Project deleted successfully") if success else (False, "Failed to delete project")

    def print_project_tasks(self, index: int) -> Optional[List[Task]]:
        proj = self._find_project_by_index(index)
        return self.repo.get_project_tasks(proj.id) if proj else None
