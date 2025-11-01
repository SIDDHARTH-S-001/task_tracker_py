import json

class TaskTrackerPy():
    def __init__(self):
        self.all_tasks, self.planned, self.active, self.complete = [], [], [], []
        self.default_status = "planned"
        self.allowed_states = ("planned", "active", "complete")
        self.default_description = ""

    def add(self, task, description):
        task = dict(task_id=len(self.all_tasks) , name=str(task).lower(), status=self.default_status, description=description)
        self.all_tasks.append(task); self.planned.append(task)
        print(f"Added '{task['name']}' to the registry, its ID is {task['task_id']}")

    def remove(self, task):
        if len(self.all_tasks) > 0:
            for i in range(len(self.all_tasks)):
                assert self.all_tasks[i]["name"] == str(task).lower(), f"The requested task {task} doesn't exist in the registry. Run 'task-cli list' to verify registry contents"
                task_status = self.all_tasks[i]["status"]
                self.all_tasks.pop(i)
                self.planned.pop(i) if task_status=="planned" else self.active.pop(i) if task_status=="active" else self.complete.pop(i) if task_status=="complete" else None
                print(print(f"Removed task '{task}' from the registry"))                
        else:
            print(f"Registry is empty")
        return self.all_tasks

    def update_status(self, task, status):
        if len(self.all_tasks) > 0:
            for i in range(len(self.all_tasks)):
                assert self.all_tasks[i]["name"] == str(task).lower(), f"The requested task {task} doesn't exist in the registry. Run 'task-cli list' to verify registry contents"
                prev_status = self.all_tasks[i]["status"]
                self.all_tasks[i]["status"] = status; print(f"Task '{task}' status updated to '{status}'") if status in self.allowed_states else print(f"Invalid status {status}") 
                t = self.all_tasks[i]
                self.planned.pop(i) if prev_status=="planned" else self.active.pop(i) if prev_status=="active" else self.complete.pop(i) if prev_status=="complete" else None
                self.planned.append(t) if status=="planned" else self.active.append(t) if status=="active" else self.complete.append(t) if status=="complete" else None
        return self.all_tasks
    
    def to_json(self, filename):
        filename = str(filename).lower() + ".json"
        contents = [self.all_tasks, self.planned, self.active, self.complete]
        with open(filename, mode="w", encoding="utf-8") as write_file:
            json.dump(contents, write_file, indent=2)

if __name__ == "__main__":
    tt = TaskTrackerPy()
    tt.add("Build Task Tracker", "Building a basic task registry program.")
    tt.update_status("Build Task Tracker", "active")
    tt.remove("Build Task Tracker")
    tt.to_json("task_register")