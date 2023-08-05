import setuptools     # import setuptools
from pathlib import Path

setuptools.setup(     # key word argument
    name="DJPDF",
    version=1.0,
    long_description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["test", "data"])   # find the packages but exclu tests and data
)