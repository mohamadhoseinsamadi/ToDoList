from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List
from app.models.task import TaskStatus


class TaskResponse(BaseModel):
    """Schema for task response"""
    id: str = Field(..., description="Task ID")
    project_id: str = Field(..., description="Project ID that this task belongs to")
    name: str = Field(..., description="Task name")
    description: Optional[str] = Field(None, description="Task description")
    status: TaskStatus = Field(..., description="Task status")
    deadline: Optional[datetime] = Field(None, description="Task deadline")
    created_time: datetime = Field(..., description="Task creation time")
    closed_at: Optional[datetime] = Field(None, description="Task closure time")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174001",
                "project_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Complete API implementation",
                "description": "Implement all API endpoints",
                "status": "todo",
                "deadline": "2025-12-01T00:00:00",
                "created_time": "2025-11-01T10:00:00",
                "closed_at": None
            }
        }
    }


class TaskListResponse(BaseModel):
    """Schema for list of tasks response"""
    tasks: List[TaskResponse] = Field(..., description="List of tasks")
    count: int = Field(..., description="Total number of tasks")

    model_config = {
        "json_schema_extra": {
            "example": {
                "tasks": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174001",
                        "project_id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "Complete API implementation",
                        "description": "Implement all API endpoints",
                        "status": "todo",
                        "deadline": "2025-12-01T00:00:00",
                        "created_time": "2025-11-01T10:00:00",
                        "closed_at": None
                    }
                ],
                "count": 1
            }
        }
    }

