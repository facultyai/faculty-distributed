from faculty import client
import os
import datetime


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


def utc_datetime_now():
    """
    Returns a string representing the current datetime in a human-readable
    format.
    
    Parameters
    ----------

    None
    
    Returns
    -------
    
    utc_datetime_now: String
        String representing the current datetime in a human-readable format.
    
    """
    now = datetime.datetime.utcnow()
    return now.strftime("%Y_%m_%d_%H_%M_%S_%f")


def most_recent_job_dirs(
    reference_dir, startswith="job_", endswith="", latest=1
):
    """
    Return a list of subdirectories in the reference directory that correspond
    to the latest runs of the parallel job. The list is sorted so that
    recent entries appear first.
    
    Parameters
    ----------
    
    reference_dir: String
        The directory where job subdirectories are created by runs of the
        parallel job.
        
    startswith: String, optional, default='job_'
        String specifying the naming convention for job subdirectories.
    
    endswith: String, optional, default = ''
        String specifying the naming convention for job subdirectories.
        
    latest: Integer, optional, default = 1
        The number of recent runs of the cross-validation job to be considered.
        Default behaviour is to return the very latest job subdirectory.
     
    Returns
    -------
    
    job_dirs: List of Strings
        Paths of subdirectories containing the results from recent jobs.
    
    """

    job_dirs = []
    for name in os.listdir(reference_dir):
        path = os.path.join(reference_dir, name)
        if os.path.isdir(path):
            if name.startswith(startswith) and name.endswith(endswith):
                job_dirs.append(path)
    return sorted(job_dirs, reverse=True)[:latest]
