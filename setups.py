from setuptools import setup, find_packages

__component_name__ = "ciggy"
__author__ = "me"
__version__ = "0.0.1"
__description__ = "-*- A Bookmarks Organizer  -*-"
__long_description__ = """"""

setup(
    name=__component_name__,
    version=__version__,
    author=__author__,
    long_description=__long_description__ if __long_description__ else __description__,
    packages=find_packages(where="."),
    package_dir={"": "."},
)
