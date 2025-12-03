from sqlalchemy import Column, String, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base


class TaskStatus(str, enum.Enum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    name = Column(String(30), nullable=False)
    description = Column(String(150), nullable=True)
    status = Column(SQLEnum(TaskStatus), default=TaskStatus.TODO)
    deadline = Column(DateTime, nullable=True)
    created_time = Column(DateTime, default=datetime.now)

    closed_at = Column(DateTime, nullable=True)

    project = relationship("Project", back_populates="tasks")
