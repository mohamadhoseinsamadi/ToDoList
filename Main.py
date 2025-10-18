from CLI import ToDoManager


def main_loop():
    todo = ToDoManager()
    while True:
        print("1: project list")
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
                if index == -1:
                    continue
                todo.view_project(index)
                print("2: tasks of this project")
                print("3: add task for this project")
                print("0: back")
                user_input = input("Choose an option: ").strip()
                print()
                if user_input=="0":
                    continue
                elif user_input=="1":
                    new_name=input("Enter new name: ")
                    new_desc=input("Enter new description (press Enter to skip): ")
                    todo.edit_project(index,new_name,new_desc)
                elif user_input=="2":
                    todo.list_project_tasks(index)
                elif user_input=="3":
                    name = input("Enter Task name: ").strip()
                    desc = input("Enter Task description (press Enter to skip): ")
                    todo.create_task(index,name,desc)

            case "2":
                name = input("Enter project name: ").strip()
                desc = input("Enter project description (press Enter to skip): ")
                todo.create_project(name, desc)

            case "0":
                print("Exiting...")
                break
            case _:
                print("???")


if __name__ == "__main__":
    main_loop()
