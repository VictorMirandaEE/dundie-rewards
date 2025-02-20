"""Setup for setuptools."""

import os

from setuptools import find_packages, setup

from dundie.settings import PROJECT_NAME


def read(*paths):
    """
    Safely read file contents.

    >>> read("project_name", "VERSION")
    '0.1.0'
    >>> read("README.md")
    ...
    """
    rootpath = os.path.dirname(__file__)
    filepath = os.path.join(rootpath, *paths)
    with open(filepath) as file:
        return file.read().strip()


def read_requirements(path: str):
    """
    Return a list of requirements from a text file.

    Args:
        path (str): path to the requirements text file.
    """
    return [
        line.strip()
        for line in read(path).split("\n")
        if not line.startswith(("#", "git+", '"', "-"))
    ]


setup(
    name=PROJECT_NAME,
    # version format is X.Y.Z (Major.Minor.Patch) - https://semver.org/
    version="0.1.6",
    description="Dunder Mifflin Rewards System",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    author="Victor Miranda",
    python_requires=">=3.10",
    url="https://github.com/VictorMirandaEE/dundie-rewards",
    # A Python package is any folder containing __init__.py
    packages=find_packages(exclude=["integration"]),
    # Include files from MANIFEST.in
    include_package_data=True,
    entry_points={"console_scripts": ["dundie = dundie.__main__:main"]},
    install_requires=read_requirements("requirements.txt"),
    extras_require={
        "test": read_requirements("requirements.test.txt"),
        "dev": read_requirements("requirements.dev.txt"),
    },
)
