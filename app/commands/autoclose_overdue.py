import schedule
from app.services.task_service import TaskService


def schedule_overdue(taskService: TaskService) -> None:
    """
    schduler

    Params:
        taskService: TaskService
    Returns:
        None
    """

    schedule.every(10).seconds.do(taskService.autoclose_overdue_tasks)
    schedule.run_all()
