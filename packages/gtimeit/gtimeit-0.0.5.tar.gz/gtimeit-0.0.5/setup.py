from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    readme = readme_file.read()


long_description = """
# gtimeit
Timer, benchmark and ressource usage tracker.
A tool for python functions. Time and compare your functions inside or outside a program.

## Benchmark

Allows to run multiple python functions a certain amount of times and to compare there respective execution times.
Similar to [timeit](https://docs.python.org/2/library/timeit.html) Display curves of all the execution times.
Prototype : benchmarking for complexity tests up to one variable parameter. The variable take all the values of a given range and the benchmarck keeps track of the executions times.

## Tracker
Allow to keep track of the execution time of some functions in a program. Useful to know which part of your program take the more time to execute.

Read the README at https://github.com/Chthi/gtimeit for more information.
"""


requirements = ["numpy>=1.18.2", "matplotlib>=3.2.1"]

setup(
    name="gtimeit",
    version="0.0.5",
    author="Thibault Charmet",
    author_email="",
    description="Timer, benchmark and ressource usage tracker. A tool for python functions. Time and compare your functions inside or outside a program.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Chthi/gtimeit",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='time benchmark track plot compare',
    python_requires='>=3.6',
)
