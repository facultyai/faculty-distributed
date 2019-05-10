# faculty-parallel

Tool running functions in paralle across multiple servers using Faculty Jobs. To access the functionality one makes use of the class:

```python
faculty_distributed.FacultyJobExecutor
```
Additional information is found in the notebook in the `examples` directory.

## Installation instructions

Clone the repository:

```bash
git clone git@github.com:facultyai/faculty-distributed.git
```

### Create an environment

You need to create an environment called `faculty_distributed` that can be applied on the distributed workers that installs `faculty-distributed`. Put the following command in the `scripts` section of the environments tab.

```bash
pip install -U git+ssh://git@github.com/facultyai/faculty-distributed.git
```

This environment should be applied to any new server that you create.

### Create a job definition

Next, create a new job definition named `distributed_{USER_NAME}`. In the `COMMAND` section, paste the following:

`faculty_distributed_jobs $path $worker_id`

Then, add a `PARAMETER` with the name `path`, of type `text` and ensure that the `Make field mandatory` box is checked. Create another `PARAMETER` named `worker_id` of type `text` and ensure that the `Make field mandatory` box is checked.

Finally, under `SERVER SETTINGS`, add `faculty_distributed` to the `ENVIRONMENTS` section.

Depending on the level of parallelisation required and how long each function takes to run it may be better to use dedicated rather than shared instances. To achieve this, click on `Large and GPU servers` under `SERVER RESOURCES`, and select an appropriate server type from the dropdown menu.

Remember to click `SAVE` when you are finished.

## Try the example
An example of excecuting a function with `faculty-distributed` is provided in the directory `examples/`. The notebook loads an example dataset, defines a function that trains a model, defines a list of arguments to be passed to the function in parallel, runs the jobs and then collects the results. The notebook will wait for the jobs to be completed before executing the remainder of the script.