from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_task_service, get_project_service
from app.services.task_service import TaskService
from app.services.project_service import ProjectService
from app.models.task import TaskStatus
from app.api.controller_schemas.requests.task_request_schema import (
    TaskCreateRequest,
    TaskUpdateRequest
)
from app.api.controller_schemas.responses.task_response_schema import (
    TaskResponse,
    TaskListResponse
)
from app.api.controller_schemas.responses.project_response_schema import MessageResponse


router = APIRouter(prefix="/projects/{project_id}/tasks", tags=["Tasks"])


@router.get(
    "/",
    response_model=TaskListResponse,
    summary="Get all tasks for a project",
    description="Retrieve a list of all tasks belonging to a specific project"
)
async def get_project_tasks(
    project_id: str,
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Get all tasks for a project.
    
    - **project_id**: The unique identifier of the project
    """
    project = project_service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    tasks = task_service.print_project_tasks(project_id=project_id)
    tasks = tasks or []
    
    return TaskListResponse(
        tasks=[TaskResponse.model_validate(t) for t in tasks],
        count=len(tasks)
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by ID",
    description="Retrieve a specific task by its ID"
)
async def get_task_by_id(
    project_id: str,
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Get a task by ID.
    
    - **project_id**: The unique identifier of the project
    - **task_id**: The unique identifier of the task
    """
    project = project_service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    task = task_service.find_task_by_id(project_id=project_id, task_id=task_id)
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    
    return TaskResponse.model_validate(task)


@router.post(
    "/",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    description="Create a new task in the specified project"
)
async def create_task(
    project_id: str,
    task_data: TaskCreateRequest,
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Create a new task.
    
    - **project_id**: The unique identifier of the project
    - **name**: Task name (required, max 30 characters)
    - **description**: Task description (optional, max 150 characters)
    - **status**: Task status (optional, default: todo)
    - **deadline**: Task deadline (optional)
    """
    project = project_service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    task_status = task_data.status if task_data.status is not None else TaskStatus.TODO
    
    success, message, created_task = task_service.create_task(
        project_id=project_id,
        title=task_data.name,
        description=task_data.description or "",
        status=task_status,
        deadline=task_data.deadline
    )
    
    if not success or not created_task:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return TaskResponse.model_validate(created_task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task",
    description="Update an existing task's details"
)
async def update_task(
    project_id: str,
    task_id: str,
    task_data: TaskUpdateRequest,
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Update a task.
    
    - **project_id**: The unique identifier of the project
    - **task_id**: The unique identifier of the task to update
    - **name**: New task name (optional)
    - **description**: New task description (optional)
    - **status**: New task status (optional)
    - **deadline**: New task deadline (optional)
    """
    project = project_service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    status_str = task_data.status.value if task_data.status is not None else None
    
    success, message = task_service.edit_task_by_id(
        project_id=project_id,
        task_id=task_id,
        new_title=task_data.name,
        new_description=task_data.description,
        status=status_str,
        new_deadline=task_data.deadline
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    updated_task = task_service.find_task_by_id(project_id=project_id, task_id=task_id)
    
    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task updated but could not be retrieved"
        )
    
    return TaskResponse.model_validate(updated_task)


@router.delete(
    "/{task_id}",
    response_model=MessageResponse,
    summary="Delete a task",
    description="Delete a task from a project"
)
async def delete_task(
    project_id: str,
    task_id: str,
    task_service: TaskService = Depends(get_task_service),
    project_service: ProjectService = Depends(get_project_service)
):
    """
    Delete a task.
    
    - **project_id**: The unique identifier of the project
    - **task_id**: The unique identifier of the task to delete
    """
    project = project_service.get_project_by_id(project_id)
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    success, message = task_service.delete_task_by_id(
        project_id=project_id,
        task_id=task_id
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in message.lower() else status.HTTP_400_BAD_REQUEST,
            detail=message
        )
    
    return MessageResponse(message=message, success=True)
