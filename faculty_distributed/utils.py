from faculty import client
import os


def job_name_to_job_id(job_name, project_id=None):
    """
    Queries faculty platform so as to convert a specified job name into its
    corresponding job id.

    Parameters
    ----------

    job_name: String
        Job name to query the platform for.

    project_id: uuid
        Unique id of the project on the platform.

    Returns
    -------

    job_id: uuid
        Unique job id corresponding to the specified job name and project.
    """

    if project_id is None:
        project_id = os.environ["FACULTY_PROJECT_ID"]
    job_client = client("job")
    for job in job_client.list(project_id):
        if job.metadata.name == job_name:
            return job.id
