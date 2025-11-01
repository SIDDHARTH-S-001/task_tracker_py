#!/usr/bin/python3
import os
import json
import argparse
import datetime

class TaskTrackerPy():
    def __init__(self, filename="default"):
        self.all_tasks, self.planned, self.active, self.complete = [], [], [], []
        self.default_status = "planned"
        self.allowed_states = ("planned", "active", "complete")
        self.default_description = ""
        self.filename = str(filename).lower() + ".json"

    def add(self, task, description):
        self.all_tasks, self.planned, self.active, self.complete = self.memory()[0], self.memory()[1], self.memory()[2], self.memory()[3]
        task = dict(task_id=len(self.all_tasks) , name=str(task).lower(), status=self.default_status, description=description, create_time=self.process_datetime(), update_time=self.process_datetime())
        self.all_tasks.append(task); self.planned.append(task)
        self.to_json(self.filename)
        print(f"Added '{task['name']}' to the registry, its ID is {task['task_id']}")

    def remove(self, task):
        self.all_tasks, self.planned, self.active, self.complete = self.memory()[0], self.memory()[1], self.memory()[2], self.memory()[3]
        if len(self.all_tasks) > 0:
            for i in range(len(self.all_tasks)):
                if self.all_tasks[i]["name"] == str(task).lower():
                    task_status = self.all_tasks[i]["status"]
                    self.all_tasks.pop(i)
                    if task_status=="planned":
                        for j in range(len(self.planned)):
                            if self.planned[j]["name"] == str(task).lower():
                                self.planned.pop(j)
                    elif task_status=="active":
                        for j in range(len(self.active)):
                            if self.active[j]["name"] == str(task).lower():
                                self.active.pop(j) 
                    elif task_status=="complete":
                        for j in range(len(self.complete)):
                            if self.complete[j]["name"] == str(task).lower():
                                self.complete.pop(j) 
                    print(f"Removed task '{task}' from the registry") 
                    break
                elif self.all_tasks[i]["name"] != str(task).lower() and (i == len(self.all_tasks)-1):
                    print(f"The requested task {task} doesn't exist in the registry, verify registry contents")
            self.to_json(self.filename)
        else:
            print(f"Registry is empty")
        return self.all_tasks

    def update_status(self, task, status):
        self.all_tasks, self.planned, self.active, self.complete = self.memory()[0], self.memory()[1], self.memory()[2], self.memory()[3]
        if len(self.all_tasks) > 0 and status in self.allowed_states:
            for i in range(len(self.all_tasks)):
                if self.all_tasks[i]["name"] == str(task).lower(): 
                    prev_status = self.all_tasks[i]["status"]
                    if status == prev_status:
                        print(f"The requested task {task} is already in the requested '{status}' status")
                        break
                    self.all_tasks[i]["status"] = status; print(f"Task '{task}' status updated to '{status}'") if status in self.allowed_states else print(f"Invalid status {status}") 
                    self.all_tasks[i]["update_time"] = self.process_datetime()
                    t = self.all_tasks[i]
                    if prev_status=="planned":
                        for j in range(len(self.planned)):
                            if self.planned[j]["name"] == str(task).lower():
                                self.planned.pop(j)
                    elif prev_status=="active":
                        for j in range(len(self.active)):
                            if self.active[j]["name"] == str(task).lower():
                                self.active.pop(j) 
                    elif prev_status=="complete":
                        for j in range(len(self.complete)):
                            if self.complete[j]["name"] == str(task).lower():
                                self.complete.pop(j) 
                    self.planned.append(t) if status=="planned" else self.active.append(t) if status=="active" else self.complete.append(t) if status=="complete" else None
                    break
                elif self.all_tasks[i]["name"] != str(task).lower() and (i == len(self.all_tasks)-1):
                    print(f"The requested task {task} doesn't exist in the registry, verify registry contents")
            self.to_json(self.filename)
        else:
            print(f"Invalid status {status}, it must be one of {self.allowed_states}")
        return self.all_tasks
    
    def process_datetime(self):
        date_time = datetime.datetime.now()
        date = date_time.strftime("%x")
        time = date_time.strftime("%X")
        date_time = str(time) + " - "+ str(date)
        return date_time
    
    def memory(self):
        if os.path.exists(self.filename):
            with open(self.filename, mode="r", encoding="utf-8") as read_file:
                current_data = json.load(read_file)      
                return current_data
        else:
            self.to_json(self.filename)
            self.memory()
    
    def format_output(self, task_list, list_type):
        print(f"----- List of {str(list_type).lower()} task -----")
        for t in task_list:
            task_id, task_name, task_status, task_description, createAt, updateAt = t["task_id"], t["name"], t["status"], t["description"], t["create_time"], t["update_time"]
            print("\nID: ", task_id)
            print("\nName: ", task_name)
            print("\nStatus: ", task_status)
            print("\nDesc : ", task_description)
            print("\nCreated At: ", createAt)
            print("\nUpdated At:", updateAt)
            print("--------------------------------\n")

    def parse_cli(self):
        parser = argparse.ArgumentParser(description="Task Registry")
        parser.add_argument("-a", "--add", type=str, nargs="+",  help="Add task to registry, pass 2 string arguments for taskname & description")
        parser.add_argument("-r", "--remove", type=str, nargs=1,  help="remove task from registry, pass 1 string argument for taskname")
        parser.add_argument("-u", "--update", type=str, nargs=2,  help="Update task in registry, pass 2 string arguments for taskname & new status")
        parser.add_argument("-s", "--show", choices=["all", "planned", "active", "complete"], default=None, help="Shows all the current tasks")
        args = parser.parse_args()
        if args.add:
            self.add(args.add[0], args.add[1] if len(args.add) > 1 else "")
        if args.remove:
            self.remove(args.remove[0])
        if args.update:
            self.update_status(args.update[0], args.update[1])
        
        current_data = self.memory()
        all_data, planned, active, complete = current_data[0], current_data[1], current_data[2], current_data[3]
        if args.show:
            match args.show:
                case "all":
                    self.format_output(all_data, "all")
                case "planned":
                    self.format_output(planned, "planned")
                case "active":
                    self.format_output(active, "active")
                case "complete":
                    self.format_output(complete, "complete")
                case _:
                    self.format_output(all_data, "all")

    def to_json(self, filename):
        contents = [self.all_tasks, self.planned, self.active, self.complete]
        with open(filename, mode="w", encoding="utf-8") as write_file:
            json.dump(contents, write_file, indent=2)

if __name__ == "__main__":
    tt = TaskTrackerPy("task_register")
    tt.parse_cli()