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

if __name__ == "__main__":
    tt = TaskTrackerPy()
    tt.add("Build Task Tracker")
