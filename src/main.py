import json

class TaskTrackerPy():
    def __init__(self):
        self.tasks = []
        self.default_status = "active"
        self.allowed_states = ("active", "complete")

    def add(self, task):
        task = dict(task_id=len(self.tasks) , name=str(task).lower(), status=self.default_status)
        self.tasks.append(task)
        print(f"Added '{task['name']}' to the registry, its ID is {task['task_id']}")

    def remove(self, task):
        print(len(self.tasks))
        if len(self.tasks) > 0:
            for i in range(len(self.tasks)):
                assert self.tasks[i]["name"] == str(task).lower(), f"The requested task {task} doesn't exist in the registry. Run 'task-cli list' to verify registry contents"
                self.tasks.pop(i)
                print(f"Removed task '{task}' from the registry")
                print(len(self.tasks))
        else:
            print(f"Registry is empty")
        return self.tasks

if __name__ == "__main__":
    tt = TaskTrackerPy()
    tt.add("Build Task Tracker")
    tt.remove("Build Task")
