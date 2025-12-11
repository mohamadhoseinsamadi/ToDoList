from pydantic import BaseModel, Field, field_validator
from typing import Optional
from app.config import MAX_PROJECT_NAME_LENGTH, MAX_PROJECT_DESCRIPTION_LENGTH


class ProjectCreateRequest(BaseModel):
    """Schema for creating a new project"""
    name: str = Field(..., min_length=1, max_length=MAX_PROJECT_NAME_LENGTH, description="Project name")
    description: Optional[str] = Field(None, max_length=MAX_PROJECT_DESCRIPTION_LENGTH, description="Project description")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not v or not v.strip():
            raise ValueError("Project name cannot be empty")
        return v.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, v):
        if len(v.split()) > MAX_PROJECT_DESCRIPTION_LENGTH:
            raise ValueError("Description must be <= 150 words")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "My Project",
                "description": "A sample project description"
            }
        }
    }


class ProjectUpdateRequest(BaseModel):
    """Schema for updating an existing project"""
    name: Optional[str] = Field(None, min_length=1, max_length=MAX_PROJECT_NAME_LENGTH, description="New project name")
    description: Optional[str] = Field(None, max_length=MAX_PROJECT_DESCRIPTION_LENGTH, description="New project description")

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (not v or not v.strip()):
            raise ValueError("Project name cannot be empty")
        return v.strip() if v else None

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Updated Project Name",
                "description": "Updated description"
            }
        }
    }

