from app.cli.cli import ToDoManager
from app.models.models import Project, Task, TaskStatus


def main_loop():
    todo = ToDoManager()
    while True:
        print("1: view project list")
        print("2: add project")
        print("0: exit")
        user_input = input("Choose an option: ").strip()
        print()
        match user_input:
            case "1":
                ok=todo.print_projects()
                if ok==False:
                    continue
                print("enter index of project to open it, or -1 to return to the main menu")
                index = int(input())
                if(index==-1):
                    continue
                if index <1 or index>len(todo.storage.projects):
                    print("invalid index")
                    continue
                while True:
                    todo.view_project(index)
                    print("1: edit project")
                    print("2: delete project")
                    print("3: tasks of this project")
                    print("4: add task for this project")
                    print("0: back")
                    user_input = input("Choose an option: ").strip()
                    print()
                    if user_input=="0":
                        break
                    elif user_input=="1":
                        new_name=input("Enter new name: ")
                        new_desc=input("Enter new description (press Enter to skip): ")
                        print()
                        todo.edit_project(index,new_name,new_desc)
                    elif user_input=="2":
                        todo.delete_project(index)
                        break
                    elif user_input=="3":
                        okay=todo.list_project_tasks(index)
                        if okay==False:
                            continue
                        print("enter index of task to open it, or -1 to return to the main menu")
                        i = int(input())
                        if i == -1:
                            continue
                        if i < 1 or i > len(todo.storage.projects[index-1].tasks):
                            print("invalid index")
                            continue
                        while True:
                            todo.view_task(index,i)
                            print("1: edit task")
                            print("2: delete task")
                            print("0: back")
                            user_input = input("Choose an option: ").strip()
                            print()
                            if user_input == "0":
                                break
                            elif user_input=="1":
                                new_name = input("Enter Task name: ").strip()
                                new_desc = input("Enter Task description (press Enter to skip): ")
                                new_stat = input("Enter status (press Enter to skip): ")
                                new_deadline = input("Enter deadline (press Enter to skip): ")
                                print()
                                todo.edit_task(index,i,new_name,new_desc,new_stat,new_deadline)
                            elif user_input=="2":
                                todo.delete_task(index,i)
                                break

                    elif user_input=="4":
                        name = input("Enter Task name: ").strip()
                        desc = input("Enter Task description (press Enter to skip): ")
                        stat= input("Enter status (press Enter to skip): ")
                        deadline=input("Enter deadline (press Enter to skip): ")
                        print()
                        todo.create_task(index,name,desc,stat,deadline)


            case "2":
                name = input("Enter project name: ").strip()
                desc = input("Enter project description (press Enter to skip): ")
                print()
                todo.create_project(name, desc)

            case "0":
                print("Exiting...")
                break
            case _:
                print("invalid command")


if __name__ == "__main__":
    main_loop()
