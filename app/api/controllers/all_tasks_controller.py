from fastapi import APIRouter, Depends, HTTPException, status
from app.api.dependencies import get_task_service
from app.services.task_service import TaskService
from app.api.controller_schemas.responses.task_response_schema import (
    TaskListResponse,
    TaskResponse
)
from app.api.controller_schemas.responses.project_response_schema import MessageResponse
from app.api.controller_schemas.requests.task_request_schema import TaskUpdateRequest

router = APIRouter(prefix="/tasks", tags=["Tasks - Global"])


@router.get(
    "/",
    response_model=TaskListResponse,
    summary="Get all tasks in the system (global)",
    description="Retrieve a list of all tasks across all projects."
)
async def get_all_tasks(
        task_service: TaskService = Depends(get_task_service)
):
    tasks = task_service.print_all_tasks()
    return TaskListResponse(
        tasks=[TaskResponse.model_validate(t) for t in tasks],
        count=len(tasks)
    )


@router.get(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Get task by global ID",
    description="Retrieve a specific task by its unique ID (globally)."
)
async def get_task_by_id(
        task_id: str,
        task_service: TaskService = Depends(get_task_service)
):
    """
    Get a task by its ID.

    - **task_id**: The unique identifier of the task
    """
    task = task_service.find_task_byid(task_id)

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return TaskResponse.model_validate(task)


@router.patch(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task by global ID",
    description="Update a task's details (name, description, status, deadline) globally."
)
async def update_task_by_id(
        task_id: str,
        task_data: TaskUpdateRequest,
        task_service: TaskService = Depends(get_task_service)
):
    """
    Update a task.

    - **task_id**: The unique identifier of the task
    - **task_data**: Fields to update
    """
    success, message = task_service.update_task_by_id(
        task_id=task_id,
        request_data=task_data
    )

    if not success:
        if message == "Task not found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=message
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=message
        )

    updated_task = task_service.find_task_byid(task_id)

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task updated but could not be retrieved"
        )

    return TaskResponse.model_validate(updated_task)



@router.delete(
    "/{task_id}",
    response_model=MessageResponse,
    summary="Delete a task by global ID",
    description="Delete a task from the system using its unique ID."
)
async def delete_task_by_id(
        task_id: str,
        task_service: TaskService = Depends(get_task_service)
):
    """
    Delete a task.

    - **task_id**: The unique identifier of the task to delete
    """
    success, message = task_service.delete_task_by_id_global(task_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message
        )

    return MessageResponse(message=message)
