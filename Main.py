from CLI import ToDoManager


def main_loop():
    todo = ToDoManager()
    while True:
        print("1: project list")
        print("2: add project")
        print("3: exit")
        user_input = input("Choose an option: ").strip()

        match user_input:
            case "1":
                print("Project list: ")
                todo.print_projects()
            case "2":
                name = input("Enter project name: ").strip()
                print(f"Adding project: {name}")

            case "3":
                print("Exiting...")

            case _:
                print("???")


if __name__ == "__main__":
    main_loop()
