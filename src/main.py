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
        for t in self.all_tasks:
            if t["name"] == task:
                print(f"The requested task {task} already exists in the registry")
                return
        task = dict(task_id=len(self.all_tasks) , name=str(task).lower(), status=self.default_status, description=description, create_time=self.process_datetime(), update_time=self.process_datetime())
        self.all_tasks.append(task); self.planned.append(task)
        self.to_json(self.filename)
        print(f"Added '{task['name']}' to the registry, its ID is {task['task_id']}")

    def remove(self, task):
        print("started remove function")
        self.all_tasks, self.planned, self.active, self.complete = self.memory()[0], self.memory()[1], self.memory()[2], self.memory()[3]
        if len(self.all_tasks) > 0:
            for i in range(len(self.all_tasks)):
                if self.all_tasks[i]["name"] == str(task).lower():
                    task_status = self.all_tasks[i]["status"]
                    print(task_status)
                    self.all_tasks.pop(i)
                    print("removed from all list")
                    if task_status=="planned":
                        for j in range(len(self.planned)):
                            if self.planned[j]["name"] == str(task).lower():
                                self.planned.pop(j)
                                print("removed from planned list"); break
                    elif task_status=="active":
                        for j in range(len(self.active)):
                            if self.active[j]["name"] == str(task).lower():
                                self.active.pop(j); break
                    elif task_status=="complete":
                        for j in range(len(self.complete)):
                            if self.complete[j]["name"] == str(task).lower():
                                self.complete.pop(j); break
                    break
                elif self.all_tasks[i]["name"] != str(task).lower() and (i == len(self.all_tasks)-1):
                    print(f"The requested task {task} doesn't exist in the registry, verify registry contents")
            print(f"Removed task '{task}' from the registry") 
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
                                self.planned.pop(j); break
                    elif prev_status=="active":
                        for j in range(len(self.active)):
                            if self.active[j]["name"] == str(task).lower():
                                self.active.pop(j); break
                    elif prev_status=="complete":
                        for j in range(len(self.complete)):
                            if self.complete[j]["name"] == str(task).lower():
                                self.complete.pop(j); break
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
        parser.add_argument("command", choices=["add", "remove", "update", "show"], help="Command to execute, pick one off [add, remove, update, show]")
        parser.add_argument("arg1", nargs="?", help="For 'add', 'remove', 'update' & 'show' methods")
        parser.add_argument("arg2", nargs="?", help="For 'add' & 'update' methods only")
        args = parser.parse_args()
        if args.command=="add":
            if not args.arg1:
                parser.error("'add' requires 'task name '& 'description' [optional]")
            self.add(args.arg1, args.arg2 or "")
        if args.command=="remove":
            if not args.arg1:
                parser.error("'remove' requires 'task name'")
            self.remove(args.arg1)
        if args.command=="update":
            if not args.arg1:
                parser.error("'update' requires 'task name'& 'status'")
            self.update_status(args.arg1, args.arg2)        
        current_data = self.memory()
        all_data, planned, active, complete = current_data[0], current_data[1], current_data[2], current_data[3]
        if args.command=="show":
            match args.arg1:
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