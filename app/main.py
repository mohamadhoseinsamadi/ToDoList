from app.cli.console import ToDoManager
from app.repositories.project_repository import InMemoryProjectRepository
from app.services.project_service import ProjectService
from app.repositories.task_repository import InMemoryTaskRepository
from app.services.task_service import TaskService


def main_loop():
    project_repo = InMemoryProjectRepository()
    project_service = ProjectService(project_repo)
    task_repo = InMemoryTaskRepository()
    task_service = TaskService(task_repo, project_repo)
    manager = ToDoManager(project_service, task_service)

    while True:
        print("=== Main Menu ===")
        print("1. List Projects")
        print("2. Create Project")
        print("0. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == "1":
            if not manager.print_projects():
                continue

            p_idx = manager._get_int("Enter project index to open (or 0 to back): ")
            if p_idx is None or p_idx == 0:
                continue

            if not manager.project_service.check_project_exists(p_idx):
                print("Error: Project not found.")
                continue

            while True:
                manager.view_project_details(p_idx)
                print("1. Edit Project")
                print("2. Delete Project")
                print("3. List Tasks")
                print("4. Add Task")
                print("0. Back")

                p_choice = input("\nChoose option: ").strip()

                if p_choice == "0":
                    break
                elif p_choice == "1":
                    manager.handle_edit_project(p_idx)
                elif p_choice == "2":
                    confirm = input("Are you sure? All tasks will be deleted (y/n): ")
                    if confirm.lower() == 'y':
                        ok, msg = manager.project_service.delete_project(p_idx)
                        print(f">> {msg}\n")
                        break
                elif p_choice == "3":
                    if manager.list_project_tasks(p_idx):
                        t_idx = manager._get_int("Enter task index to view/edit (or 0 to back): ")
                        if t_idx is None or t_idx == 0: continue

                        if not manager.task_service.check_task_exists(p_idx, t_idx):
                            print("Error: Task not found.")
                            continue

                        while True:
                            manager.view_task_details(p_idx, t_idx)
                            print("1. Edit Task")
                            print("2. Delete Task")
                            print("0. Back")
                            t_choice = input("Choose: ").strip()

                            if t_choice == "0":
                                break
                            elif t_choice == "1":
                                manager.handle_edit_task(p_idx, t_idx)
                            elif t_choice == "2":
                                ok, msg = manager.task_service.delete_task(p_idx, t_idx)
                                print(f">> {msg}\n")
                                break

                elif p_choice == "4":
                    manager.handle_add_task(p_idx)

        elif choice == "2":
            manager.handle_add_project()

        elif choice == "0":
            print("exiting...")
            break
        else:
            print("Invalid command.")


if __name__ == "__main__":
    main_loop()
