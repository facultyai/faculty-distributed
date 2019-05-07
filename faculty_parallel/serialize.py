import distributed
import os
import cloudpickle
import time
from faculty import client
from faculty_parallel.utils import utc_datetime_now


class ParallelJobs:
    def __init__(self, project_id, job_id):
        """
        Run generic python function in parallel on Faculty Jobs
        """
        self.project_id = project_id
        self.job_id = job_id
        self.job_client = client("job")
        self.user = os.environ["USER_NAME"]

        filename = "job_" + utc_datetime_now()

        path = os.environ["JOB_PATH"]

        self.output_dir = os.path.join(path, filename, "output")
        self.func_dir = os.path.join(path, filename, "func")

        for jobs_dir in [self.output_dir, self.func_dir]:
            if not os.path.exists(jobs_dir):
                os.makedirs(jobs_dir)

    def _collect_output(self, args_list):
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
                os.path.join(self.output_dir, f"out_{i}.pkl"), "rb"
            ) as f:
                out.append(cloudpickle.load(f))
        return out

    def parmap(self, func, args_list):
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
            [{"args_num": f"{i}"} for i in range(len(args_list))],
        )
        self._wait()
        output = self._collect_output(args_list)
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
        with open(os.path.join(self.func_dir, "func.txt"), "wb") as f:
            f.write(func_dict["function"])
        for i, args in enumerate(args_list):
            func_dict = distributed.worker.dumps_task((func, *args))
            with open(os.path.join(self.func_dir, f"args_{i}.txt"), "wb") as f:
                f.write(func_dict["args"])

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
