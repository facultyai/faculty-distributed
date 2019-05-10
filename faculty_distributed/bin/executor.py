import cloudpickle
import os
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
        worker id

    """
    with open(os.path.join(path, "func/func"), "rb") as f:
        func = cloudpickle.load(f)
    with open(os.path.join(path, "func/args_{}".format(n)), "rb") as f:
        arg = cloudpickle.load(f)
    out = func(*arg)
    with open(os.path.join(path, "output/out_{}.pkl".format(n)), "wb") as f:
        cloudpickle.dump(out, f)
