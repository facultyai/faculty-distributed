import cloudpickle
import os
import sys
import click
from faculty_parallel.utils import most_recent_job_dirs


@click.command()
@click.argument("n")
def execute_func(n):
    """
    Loads function and arguments from binary serialisation, executes function
    and pickles the output. Output of function is generic. 
    Parameters
    ----------
    path: str
        path to folders to save functions and save output
    n: int 
        job number
    
    """
    path = most_recent_job_dirs(os.environ["JOB_PATH"])[0]

    with open(os.path.join(path, "func/func.txt"), "rb") as f:
        func = cloudpickle.load(f)
    with open(os.path.join(path, f"func/args_{n}.txt"), "rb") as f:
        arg = cloudpickle.load(f)
    out = func(*arg)
    with open(os.path.join(path, f"output/out_{n}.pkl"), "wb") as f:
        cloudpickle.dump(out, f)
    return None
