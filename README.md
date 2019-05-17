# faculty-distributed

Tool running functions in parallel across multiple servers using Faculty Jobs. To access the functionality one makes use of the class:

```python
faculty_distributed.FacultyJobExecutor
```

Additional information is found in the notebook in the `examples` directory.

## Installation

Either install using pip,

```bash
pip install faculty-distributed
```

or clone the repository in a directory of your choosing and install from the local copy

```bash
git clone git@github.com:facultyai/faculty-distributed.git
cd faculty-distributed
pip install .
```

## Set up
### Create an environment

You need to create an environment called `faculty_distributed` that installs `faculty-distributed`. It is recommended that the faculty-distributed package is installed through it's own environment, as it can then be kept clean for use on any distributed job.

This environment need to be applied on the server that calls the class as well as on the distributed worker servers via the jobs tab (see below).

### Create a job definition

Next, create a new job definition named `distributed_example`. In the `COMMAND` section, paste the following:

```bash
faculty_distributed_job $path $worker_id
```

Then, add a `PARAMETER` with the name `path`, of type `text` and ensure that the `Make field mandatory` box is checked. Create another `PARAMETER` named `worker_id` of type `text` and ensure that the `Make field mandatory` box is checked.

Finally, under `SERVER SETTINGS`, add `faculty_distributed` to the `ENVIRONMENTS` section. Note that any libraries used in the function to be executed that are not installed automatically on Faculty servers need to be installed on the job server via a separate environment. 

Depending on the level of parallelisation required and how long each function takes to run it may be better to use dedicated rather than shared instances. To achieve this, click on `Large and GPU servers` under `SERVER RESOURCES`, and select an appropriate server type from the dropdown menu.

Remember to click `SAVE` when you are finished.

## Usage
Import the `faculty-distributed` module and find the faculty platform project ID and job ID. Here the job name is `distributed_example`. 

```python
import faculty_distributed
import os

project_id = os.getenv['project_id']
job_id = faculty_distributed.job_name_to_job_id("distributed_example")

```

Then define function to be sent to distributed workers and a list of arguments to be sent the workers.
```python
def foo(x, y):
    return 2*x + y
    
args_list = [[1, 2], [2, 3], [3, 4]]
```

Finally, instantiate the class `FacultyJobExecutor`, passing the project and job IDs. Optional arguments are `clean`, a boolean [default = True] that determines whether temporary files created for the run are deleted immediately after the completion of the job, and `tmpdir_prefix`, a string [default = '/project/.faculty-distributed'] that defines the path to where the temporary directory is created. 

Call `map`, passing the function and the list of arguments, to execute the function. Once `map` has been called, a job will start with as many subruns as there are arguments passed. The output of these subruns will be returned as a list. 

```python
fje = faculty_distributed.FacultyJobExecutor(project_id, job_id)

output = fje.map(foo, args_list)


```

## Try the example
An example of excecuting a function with `faculty-distributed` is provided in the directory `examples/`. The notebook loads an example dataset, defines a function that trains a model, defines a list of arguments to be passed to the function in parallel, runs the jobs and then collects the results. The notebook will wait for the jobs to be completed before executing the remainder of the script.