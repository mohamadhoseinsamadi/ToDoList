from datetime import datetime
from app.db.session import SessionLocal
from app.models.task import Task, TaskStatus


def close_overdue_tasks():
    session = SessionLocal()
    try:
        now = datetime.now()
        overdue_tasks = session.query(Task).filter(
            Task.deadline < now,
            Task.status != TaskStatus.DONE
        ).all()

        print(f"Found {len(overdue_tasks)} overdue tasks.")

        for task in overdue_tasks:
            print(f"Closing task: {task.name}")
            task.status = TaskStatus.DONE
            task.closed_at = now

        session.commit()
        print("All overdue tasks closed.")
    except Exception as e:
        print(f"Error: {e}")
        session.rollback()
    finally:
        session.close()


if __name__ == "__main__":
    close_overdue_tasks()