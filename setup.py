from setuptools import setup

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
    license="",
    packages=["faculty_parallel", "faculty_parallel.bin"],
    entry_points={
        "console_scripts": [
            "faculty_parallel_jobs"
            + " = "
            + "faculty_parallel.bin.run_jobs:main"
        ]
    },
    zip_safe=False,
    
)
