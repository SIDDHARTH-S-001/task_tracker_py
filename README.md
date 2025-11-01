# task_tracker_py
This repository focuses on a  task tracking program, the backend runs python while commands operational on any linux system through CLI

This project is a submission to [roadmap.sh](https://roadmap.sh/), here's the [Project URL](https://roadmap.sh/projects/task-tracker), and link to this [solution](https://roadmap.sh/projects/task-tracker/solutions?u=6904e2c9b0418a041edd8570) on readmap.sh


## Instructions of use
Clone is repository through </br>
```
git clone https://github.com/SIDDHARTH-S-001/task_tracker_py.git
```

### (Option 1): Directly running main script
```
cd task_tracker_py/src
chmod +x main.py
python main.py --help                              # or use the '-h' flag to get a general information about the code
```

To add a task
```
python main.py add <task_name> <description>[optional]
```
To remove a task
```
python main.py remove <task_name>

```
To change the status of a task
```
python main.py update <task_name> <new_status>     # new_status - ["planned", "active", "complete"]
```
To show the list of tasks
```
python main.py show <list_name>                    # list_name - ["all", "planned", "complete"]
```

### (Option 2): Running through shell (Linux)
```
cd task_tracker_py/src
source setup.sh
```
To add a task
```
task-cli add <task_name> <description>[optional]
```
To remove a task
```
task-cli remove <task_name>

```
To change the status of a task
```
task-cli update <task_name> <new_status>     # new_status - ["planned", "active", "complete"]
```
To show the list of tasks
```
task-cli show <list_name>                    # list_name - ["all", "planned", "complete"]
```
For help, 
```
task-cli --help                              # or use the '-h' flag to get a general information about the code
```

## Notes
1) While following Option 2 (Shell), ensure the hashbang line at the start of main.py is correct. This can be found using, 
`which python` or `which python3`

### References
[Running Python scripts with CLI args](https://medium.com/@evaGachirwa/running-python-script-with-arguments-in-the-command-line-93dfa5f10eff) <br/>
[JSON](https://realpython.com/python-json/#introducing-json) <br/>
[Datetime](https://www.w3schools.com/python/python_datetime.asp) <br/>
[Argparse](https://docs.python.org/3/howto/argparse.html) </br>
[Creating README](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#headings) <br/>