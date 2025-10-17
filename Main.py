class Project:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)

    def delete_task(self, task_id):
        self.tasks = [t for t in self.tasks if t.id != task_id]


class ToDoManager:
    def __init__(self):
        self.projects = []
        self.next_proj_id = 1

    def add_project(self):
        pass
    def edit_project(self):
        pass
    def print_projects(self):
        pass




    def create_project(self, name, description):
        proj = Project(self.next_proj_id, name, description)
        self.projects.append(proj)
        self.next_proj_id += 1

    def find_project(self, proj_id):
        for p in self.projects:
            if p.id==proj_id:
                return p
        raise KeyError("پروژه یافت نشد")
def main_loop():
    todo=ToDoManager()
    while True:
        print("1: project list")
        print("2: add project")
        print("3: exit")
        user_input = input("Choose an option: ").strip()

        match user_input:
            case "1":
                print("Project list: ")
                todo.print_projects()
                break
            case "2":
                name = input("Enter project name: ").strip()
                print(f"Adding project: {name}")
                break
            case "3":
                print("Exiting...")
                break
            case _:
                print("???")


if __name__ == "__main__":
    main_loop()


