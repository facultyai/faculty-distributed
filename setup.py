from setuptools import setup, find_packages

setup(
    name="faculty-parallel",
    version="0.0.1",
    install_requires=[
        "click",
        "faculty",
        "distributed",
    ],
    description=(
        "Run functions in parallel on jobs"
    ),
    author="Faculty Science Ltd.",
    license="Apache Software License",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "faculty_parallel_jobs = faculty_parallel.bin.run_jobs:execute_func"
        ]
    },
)
