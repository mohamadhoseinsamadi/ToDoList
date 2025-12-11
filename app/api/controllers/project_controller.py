from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_project_service
from app.services.project_service import ProjectService
from app.api.controller_schemas.requests.project_request_schema import (
    ProjectCreateRequest,
    ProjectUpdateRequest
)
from app.api.controller_schemas.responses.project_response_schema import (
    ProjectResponse,
    ProjectListResponse,
    MessageResponse
)


router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get(
    "/",
    response_model=ProjectListResponse,
    summary="Get all projects",
    description="Retrieve a list of all projects in the system"
)
async def get_all_projects(
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Get all projects.
    
    Returns a list of all projects with their details.
    """
    projects = project_service.print_all_projects()
    return ProjectListResponse(
        projects=[ProjectResponse.model_validate(p) for p in projects],
        count=len(projects)
    )


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Get project by ID",
    description="Retrieve a specific project by its ID"
)
async def get_project_by_id(
    project_id: str,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Get a project by ID.
    
    - **project_id**: The unique identifier of the project
    """
    project = project_service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return ProjectResponse.model_validate(project)


@router.post(
    "/",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new project",
    description="Create a new project with the provided details"
)
async def create_project(
    project_data: ProjectCreateRequest,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Create a new project.
    
    - **name**: Project name (required, max 30 characters)
    - **description**: Project description (optional, max 150 characters)
    """
    success, message, created_project = project_service.add_project(
        name=project_data.name,
        description=project_data.description or ""
    )
    
    if not success or not created_project:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return ProjectResponse.model_validate(created_project)


@router.put(
    "/{project_id}",
    response_model=ProjectResponse,
    summary="Update a project",
    description="Update an existing project's details"
)
async def update_project(
    project_id: str,
    project_data: ProjectUpdateRequest,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Update a project.
    
    - **project_id**: The unique identifier of the project to update
    - **name**: New project name (optional)
    - **description**: New project description (optional)
    """
    success, message = project_service.edit_project_by_id(
        project_id=project_id,
        new_name=project_data.name,
        new_description=project_data.description
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    updated_project = project_service.get_project_by_id(project_id)
    
    if not updated_project:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Project updated but could not be retrieved"
        )
    
    return ProjectResponse.model_validate(updated_project)


@router.delete(
    "/{project_id}",
    response_model=MessageResponse,
    summary="Delete a project",
    description="Delete a project and all its associated tasks"
)
async def delete_project(
    project_id: str,
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Delete a project.
    
    - **project_id**: The unique identifier of the project to delete
    
    **Note**: This will also delete all tasks associated with this project.
    """
    success, message = project_service.delete_project_by_id(project_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return MessageResponse(message=message, success=True)
