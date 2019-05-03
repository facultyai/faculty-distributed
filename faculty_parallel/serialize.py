import distributed
import os
import cloudpickle
import time
from faculty import client


class ParallelJobs:
    def __init__(self, path, project_id, job_id):
        """
        Run generic python function in parallel on Faculty Jobs
        """
        self.path = path
        self.project_id = project_id
        self.job_id = job_id
        self.job_client = client("job")

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
        with open(os.path.join(self.path, "saved_funcs/func.txt"), "wb") as f:
            f.write(func_dict["function"])
        for i, args in enumerate(args_list):
            func_dict = distributed.worker.dumps_task((func, *args))
            with open(
                os.path.join(self.path, f"saved_funcs/args_{i}.txt"), "wb"
            ) as f:
                f.write(func_dict["args"])

    def _wait(self):
        """
        Wait for jobs to finish
        """
        run = self.job_client.get_run(
            self.project_id, 
            self.job_id, 
            self.run_id
        )
        while run.ended_at is None:
            time.sleep(1)
            run = self.job_client.get_run(
                self.project_id, 
                self.job_id, 
                self.run_id
            )

    def parmap(self, func, args_list):
        self._pickle_func(func, args_list)
        
        self.run_id = self.job_client.create_run(
            self.project_id,
            self.job_id,
            [{"in_path": self.path, "args_num": f"{i}"} for i in range(len(args_list))],
        )
        self._wait()
        return self._collect_output(args_list)
        
        

    def _collect_output(self, args_list):
        """
        Collect output of jobs
        Parameters
        ----------
        args_list
            list of lists of arguments that were iterated over in parallel
        """
        out = []
        for i, _ in enumerate(args_list):
            with open(
                os.path.join(self.path, f"output/out_{i}.pkl"), "rb"
            ) as f:
                out.append(cloudpickle.load(f))
        return out
