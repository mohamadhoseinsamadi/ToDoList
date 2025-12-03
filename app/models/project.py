from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    name = Column(String(30), unique=True, nullable=False)
    description = Column(String(150), nullable=True)
    created_time = Column(DateTime, default=datetime.now)

    tasks = relationship("Task", back_populates="project", cascade="all, delete-orphan")
