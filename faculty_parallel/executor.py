import cloudpickle
import os
import sys


def execute_funcs(path, n):
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
    with open(os.path.join(path, "saved_funcs/func.txt"), "rb") as f:
        func = cloudpickle.load(f)
    with open(os.path.join(path, f"saved_funcs/args_{n}.txt"), "rb") as f:
        arg = cloudpickle.load(f)
    out = func(*arg)
    with open(os.path.join(path, f"output/out_{n}.pkl"), "wb") as f:
        cloudpickle.dump(out, f)
    return None


if __name__ == "__main__":
    print(sys.argv)
    path = sys.argv[1]
    n = sys.argv[2]
    execute_funcs(path, n)
