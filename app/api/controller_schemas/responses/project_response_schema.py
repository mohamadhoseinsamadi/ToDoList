from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class ProjectResponse(BaseModel):
    """Schema for project response"""
    id: str = Field(..., description="Project ID")
    name: str = Field(..., description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    created_time: datetime = Field(..., description="Project creation time")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "My Project",
                "description": "A sample project",
                "created_time": "2025-11-01T10:00:00"
            }
        }
    }


class ProjectListResponse(BaseModel):
    """Schema for list of projects response"""
    projects: List[ProjectResponse] = Field(..., description="List of projects")
    count: int = Field(..., description="Total number of projects")

    model_config = {
        "json_schema_extra": {
            "example": {
                "projects": [
                    {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "name": "My Project",
                        "description": "A sample project",
                        "created_time": "2025-11-01T10:00:00"
                    }
                ],
                "count": 1
            }
        }
    }


class MessageResponse(BaseModel):
    """Schema for simple message response"""
    message: str = Field(..., description="Response message")
    success: bool = Field(..., description="Operation success status")

    model_config = {
        "json_schema_extra": {
            "example": {
                "message": "Operation completed successfully",
                "success": True
            }
        }
    }

