from setuptools import setup, find_packages

setup(
    name="faculty-distributed",
    install_requires=["click", "cloudpickle", "distributed", "faculty"],
    description="Distributed execution on faculty platform",
    author="Faculty",
    license="Apache Software License",
    packages=find_packages(),
    use_scm_version={"version_scheme": "post-release"},
    setup_requires=["setuptools_scm"],
    entry_points={
        "console_scripts": [
            "faculty_distributed_job = faculty_distributed.bin.executor:execute_on_worker"  # noqa
        ]
    },
)
