import os

from setuptools import find_packages
from setuptools import setup

__version__ = "0.1.1"


def read(filename: str) -> str:
    filename = os.path.join(os.path.dirname(__file__), filename)
    with open(filename, "r", encoding="utf-8") as input_file:
        README = input_file.read()

    return README


setup(
    author="Nils Müller",
    author_email="shimst3r@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    description="Python toolbag, like a toolbox, but more flexible!",
    install_requires=["typer"],
    license="MIT",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    name="toolbag",
    packages=find_packages(exclude=("tests",)),
    python_requires=">=3.7, <4",
    url="https://github.com/shimst3r/toolbag",
    version=__version__,
)
