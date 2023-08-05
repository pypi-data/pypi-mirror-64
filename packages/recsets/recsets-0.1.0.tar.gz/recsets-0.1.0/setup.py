from setuptools import setup, find_packages
from pathlib import Path

here = Path(__file__).resolve().parent
long_description = here.joinpath("README.md").read_text()
requirements = here.joinpath("requirements.txt").read_text().split("\n")
version = here.joinpath("VERSION").read_text()

setup(
    name="recsets",
    version=version,
    description="recsets: portable recommendation datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/micaleel/recsets",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
)
