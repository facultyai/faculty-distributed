import cloudpickle
import distributed
import os
import time
import shutil
import uuid

from faculty import client


class DistributedCompute:
    def __init__(
        self, project_id, job_id, clean=True, path="/project/.faculty-parallel"
    ):
        """
        Run generic python function in parallel on Faculty Jobs
        """
        self.project_id = project_id
        self.job_id = job_id
        self.job_client = client("job")
        
        self.clean = clean

        self.path = os.path.join(path, str(uuid.uuid4()))

        for jobs_dir in [
            os.path.join(path, "output"), os.path.join(path, "func")
        ]:
            os.makedirs(jobs_dir)

    def collect_output(self, args_list):
        """
        Collect output of jobs
        
        Parameters
        ----------
        args_list: list
            list of lists of arguments that were iterated over in parallel
        
        Returns
        -------
        out: list
            list of outputs of function from each job
        """
        out = []
        for i in range(len(args_list)):
            with open(
                os.path.join(self.path, f"output/out_{i}.pkl"), "rb"
            ) as f:
                out.append(cloudpickle.load(f))

        return out

    def distribute(self, func, args_list):
        """
        Execute function for each set of arguments in list in parallel using
        Faculty Jobs.
        
        Parameters
        ----------
        func: function object
            generic python function
        args_list: list
            list of lists of arguments to be iterated over in parallel
        
        Returns
        -------
        output: list
            list of outputs of function from each job
        
        """
        self._pickle_func(func, args_list)

        self.run_id = self.job_client.create_run(
            self.project_id,
            self.job_id,
            [
                {"path": self.path, "args_num": f"{i}"} 
                for i in range(len(args_list))
            ],
        )
        self._wait()
        output = self.collect_output(args_list)
        
        if self.clean:
            self.remove_directories()

        return output

    def _pickle_func(self, func, args_list):
        """
        Serialise function and arguments list
        
        Parameters
        ----------
        func: function object
            generic python function
        args_list: list
            list of lists of arguments to be iterated over in parallel
        """
        func_dict = distributed.worker.dumps_task((func,))
        
        with open(os.path.join(self.path, "func/func.txt"), "wb") as f:
            f.write(func_dict["function"])
            
        for i, args in enumerate(args_list):
            func_dict = distributed.worker.dumps_task((func, *args))
            with open(os.path.join(self.path, f"func/args_{i}.txt"), "wb") as f:
                f.write(func_dict["args"])

    def remove_directories(self):
        """Remove files and directories associated with this job"""
        shutil.rmtree(self.path)

    def _wait(self):
        """
        Cause execution to wait for jobs to finish
        """
        run = self.job_client.get_run(
            self.project_id, self.job_id, self.run_id
        )
        while run.ended_at is None:
            time.sleep(1)
            run = self.job_client.get_run(
                self.project_id, self.job_id, self.run_id
            )
