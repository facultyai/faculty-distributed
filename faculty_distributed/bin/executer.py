import cloudpickle
import os
import sys
import click


@click.command()
@click.argument("path")
@click.argument("n")
def execute_on_worker(path, n):
    """
    Loads function and arguments from binary serialisation, executes function
    and pickles the output. Output of function is generic. 
    Parameters
    ----------
    path: str
        path to directory to load function and arguments and save output
    n: int 
        worker number
    
    """
    with open(os.path.join(path, "func/func.txt"), "rb") as f:
        func = cloudpickle.load(f)
    with open(os.path.join(path, f"func/args_{n}.txt"), "rb") as f:
        arg = cloudpickle.load(f)
    out = func(*arg)
    with open(os.path.join(path, f"output/out_{n}.pkl"), "wb") as f:
        cloudpickle.dump(out, f)
    return None
