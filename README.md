# faculty-parallel

Tool running functions in paralle across multiple servers using Faculty Jobs. To access the functionality one makes use of the class:

```python
faculty_parallel.serialize.ParallelJobs
```
Additional information is found in the notebooks of the `examples` directory.

## Developer installation instructions

#### Select a username
Before beginning the installation process, pick an appropriate username, such as `foo`. This does not necessarily need to match your faculty platform username. In the following instructions, your selected username will be referred to as `{USER_NAME}`.

#### Select a base directory
The base directory is the location where the function, arguments and output of the parallelised runs will be saved.

#### Clone the repository
Create the folder `/project/{USER_NAME}`. Then, run the commands:

```bash
cd /project/{USER_NAME}
git clone git+ssh://git@bitbucket.org/theasi/faculty-parallel.git
```

##### Create an environment

Next, create an environment in your project named `faculty_parallel_{USER_NAME}`.

In this environment, under `SCRIPTS`, paste in the following code to the `BASH` section, remembering to change the `USER_NAME` definition on the second line to your selected `{USER_NAME}`, and the `JOB_PATH` environment variable:

```bash
# Remember to change username and job path!
USER_NAME=laurence
JOB_PATH=/project/$USER_NAME/jobs/

# Install faculty-parallel from local repository.
pip install /project/$USER_NAME/faculty-parallel/

# Turn USER_NAME into an environment variable.
echo "export USER_NAME=$USER_NAME" > /etc/faculty_environment.d/app.sh
echo "export JOB_PATH=$JOB_PATH" >> /etc/faculty_environment.d/app.sh
if [[ -d /etc/service/jupyter ]] ; then 
  sudo sv restart jupyter
fi
```

This environment should be applied to any new server that you create.

#### Create a job definition

Next, create a new job definition named `parallel_{USER_NAME}`. In the `COMMAND` section, paste the following:

`faculty_parallel_jobs $args_num`

Then, add a `PARAMETER` with the name `args_num`, orf type `text` and ensure that the `Make field mandatory` box is checked.

Finally, under `SERVER SETTINGS`, add `faculty_parallel_{USER_NAME}` to the `ENVIRONMENTS` section.

Depending on the level of parallelisation required and how long each function takes to run it may be better to use dedicated rather than shared instances. To achieve this, click on `Large and GPU servers` under `SERVER RESOURCES`, and select an appropriate server type from the dropdown menu.

Remember to click `SAVE` when you are finished.

## Try the example
An example of parallelising a function with `faculty-parallel` is provided in the directories `examples/`. The notebook loads an example dataset, defines a function that trains a model, defines a list of arguments to be passed to the function in parallel, runs the jobs and then collects the results. The notebook will wait for the jobs to be completed before executing the remainder of the script.