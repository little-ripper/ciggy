from setuptools import setup, find_packages

__component_name__ = "ciggy"
__author__ = "me"
__version__ = "0.0.1"

setup(
    name=__component_name__,
    version=__version__,
    author=__author__,
    long_description=open('README').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(where="."),
    package_dir={"": "."},
)
