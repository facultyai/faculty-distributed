import cloudpickle
import distributed
import os
import time
import shutil
import tempfile

from faculty import client


class FacultyJobExecutor:
    """
    Run generic python function in parallel on Faculty Jobs

    Parameters
    ----------
    project_id: str
        ID of project on Faculty platform.
    job_id: str
        ID of job set up in Jobs tab of Faculty platform.
    clean: bool, default=True
        If True, temporary directory used to pass files to and from workers
        will be removed once workers are finished. If False, temporary files
        will be left on the workspace.
    tmpdir_prefix: str, default=None
        Root directory for temporary directory to be created in. If None,
        temporary directory will be created in "/project/.faculty-distributed".
    """

    def __init__(self, project_id, job_id, clean=True, tmpdir_prefix=None):
        self.project_id = project_id
        self.job_id = job_id
        self.job_client = client("job")

        self.clean = clean
        self.tmpdir_prefix = tmpdir_prefix

    def map(self, func, args_sequence):
        """
        Execute function for each set of arguments in list in parallel using
        Faculty Jobs. Kwargs are currently unsupported.

        Parameters
        ----------
        func: function object
            generic python function
        args_sequence: list
            list of lists of arguments to be iterated over in parallel

        Returns
        -------
        output: list
            list of outputs of function from each job

        Example usage:

        Create environments and a job as described in the README file.

        Define function to be sent to distributed workers and a list of
        arguments to be sent the workers.

        >>> def foo(x, y):
        >>>    return 2*x + y
        >>>
        >>> args_list = [[1, 2], [2, 3], [3, 4]]

        Instantiate the class FacultyJobExecutor, passing the project and
        job IDs. Then call map, passing the function and the list of arguments,
        to execute the function.

        >>> fje = faculty_distributed.FacultyJobExecutor(project_id, job_id)
        >>> output = fje.map(foo, args_list)
        """
        self._make_dirs()

        self._pickle_func(func, args_sequence)

        self.run_id = self.job_client.create_run(
            self.project_id,
            self.job_id,
            [
                {"path": self.tmpdir, "worker_id": str(i)}
                for i in range(len(args_sequence))
            ],
        )
        self._wait()
        output = self._collect_output(args_sequence)

        if self.clean:
            self._remove_directories()

        return output

    def _collect_output(self, args_sequence):
        """
        Collect output of jobs

        Parameters
        ----------
        args_sequence: list
            list of lists of arguments that were iterated over in parallel

        Returns
        -------
        out: list
            list of outputs of function from each job
        """
        out = []
        for i in range(len(args_sequence)):
            with open(
                os.path.join(self.tmpdir, "output/out_{}.pkl".format(i)), "rb"
            ) as f:
                out.append(cloudpickle.load(f))

        return out

    def _make_dirs(self):
        """Make temporary directories"""
        if self.tmpdir_prefix is None:
            self.tmpdir = tempfile.mkdtemp(
                prefix="/project/.faculty-distributed"
            )
        else:
            self.tmpdir = tempfile.mkdtemp(prefix=self.tmpdir_prefix)

        for jobs_dir in [
            os.path.join(self.tmpdir, "output"),
            os.path.join(self.tmpdir, "func"),
        ]:
            os.makedirs(jobs_dir)

    def _pickle_func(self, func, args_sequence):
        """
        Serialise function and arguments list

        Parameters
        ----------
        func: function object
            generic python function
        args_sequence: list
            list of lists of arguments to be iterated over in parallel
        """
        func_dict = distributed.worker.dumps_task((func,))

        with open(os.path.join(self.tmpdir, "func/func"), "wb") as f:
            f.write(func_dict["function"])

        for i, args in enumerate(args_sequence):
            func_dict = distributed.worker.dumps_task(tuple([func] + args))
            with open(
                os.path.join(self.tmpdir, "func/args_{}".format(i)), "wb"
            ) as f:
                f.write(func_dict["args"])

    def _remove_directories(self):
        """Remove files and directories associated with this job"""
        shutil.rmtree(self.tmpdir)

    def _wait(self):
        """Cause execution to wait for jobs to finish"""
        run = self.job_client.get_run(
            self.project_id, self.job_id, self.run_id
        )
        while run.ended_at is None:
            time.sleep(1)
            run = self.job_client.get_run(
                self.project_id, self.job_id, self.run_id
            )
