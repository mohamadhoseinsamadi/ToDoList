from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime
from app.models.task import TaskStatus
from app.config import MAX_TASK_NAME_LENGTH, MAX_TASK_DESCRIPTION_LENGTH


class TaskCreateRequest(BaseModel):
    """Schema for creating a new task"""
    name: str = Field(..., min_length=1, max_length=MAX_TASK_NAME_LENGTH, description="Task name")
    description: Optional[str] = Field(None, max_length=MAX_TASK_DESCRIPTION_LENGTH, description="Task description")
    status: Optional[TaskStatus] = Field(TaskStatus.TODO, description="Task status")
    deadline: Optional[datetime] = Field(None, description="Task deadline")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Task name cannot be empty")
        elif len(v.split()) > MAX_TASK_NAME_LENGTH:
            raise ValueError("name must be <= 30 words")
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v):
        if len(v.split()) > MAX_TASK_DESCRIPTION_LENGTH:
            raise ValueError("Description must be <= 150 words")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Complete API implementation",
                "description": "Implement all API endpoints",
                "status": "todo",
                "deadline": "2025-12-01T00:00:00"
            }
        }
    }


class TaskUpdateRequest(BaseModel):
    """Schema for updating an existing task"""
    name: Optional[str] = Field(None, min_length=1, max_length=MAX_TASK_NAME_LENGTH, description="New task name")
    description: Optional[str] = Field(None, max_length=MAX_TASK_DESCRIPTION_LENGTH, description="New task description")
    status: Optional[TaskStatus] = Field(None, description="New task status")
    deadline: Optional[datetime] = Field(None, description="New task deadline")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Task name cannot be empty")
        return v.strip() if v else None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Updated Task Name",
                "description": "Updated description",
                "status": "doing",
                "deadline": "2025-12-15T00:00:00"
            }
        }
    }

