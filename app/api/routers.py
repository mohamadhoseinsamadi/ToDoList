from fastapi import APIRouter
from app.api.controllers import project_controller, task_controller,all_tasks_controller

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(project_controller.router)
api_router.include_router(task_controller.router)
api_router.include_router(all_tasks_controller.router)
