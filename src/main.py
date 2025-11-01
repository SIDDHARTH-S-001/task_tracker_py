import json
import argparse
import datetime

class TaskTrackerPy():
    def __init__(self):
        self.all_tasks, self.planned, self.active, self.complete = [], [], [], []
        self.default_status = "planned"
        self.allowed_states = ("planned", "active", "complete")
        self.default_description = ""

    def add(self, task, description):
        task = dict(task_id=len(self.all_tasks) , name=str(task).lower(), status=self.default_status, description=description, create_time=self.process_datetime(), update_time=self.process_datetime())
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
                self.all_tasks[i]["update_time"] = self.process_datetime()
                t = self.all_tasks[i]
                self.planned.pop(i) if prev_status=="planned" else self.active.pop(i) if prev_status=="active" else self.complete.pop(i) if prev_status=="complete" else None
                self.planned.append(t) if status=="planned" else self.active.append(t) if status=="active" else self.complete.append(t) if status=="complete" else None
        return self.all_tasks
    
    def process_datetime(self):
        date_time = datetime.datetime.now()
        date = date_time.strftime("%x")
        time = date_time.strftime("%X")
        date_time = str(time) + " - "+ str(date)
        return date_time
    
    def parse_cli(self):
        parser = argparse.ArgumentParser(description="Task Registry")
        parser.add_argument("-a", "--add", type=str, nargs="+",  help="Add task to registry, pass 2 string arguments for taskname & description")
        parser.add_argument("-r", "--remove", type=str, nargs=1,  help="remove task from registry, pass 1 string argument for taskname")
        parser.add_argument("-u", "--update", type=str, nargs=2,  help="Update task in registry, pass 2 string arguments for taskname & new status")
        args = parser.parse_args()
        print(args)
        if args.add:
            self.add(args.add[0], args.add[1] if len(args.add) > 1 else "")
        if args.remove:
            self.remove(args.remove[0])
        if args.update:
            self.update_status(args.update[0], args.update[1])
    
    def to_json(self, filename):
        filename = str(filename).lower() + ".json"
        contents = [self.all_tasks, self.planned, self.active, self.complete]
        with open(filename, mode="w", encoding="utf-8") as write_file:
            json.dump(contents, write_file, indent=2)

if __name__ == "__main__":
    tt = TaskTrackerPy()
    tt.parse_cli()
    tt.to_json("task_register")