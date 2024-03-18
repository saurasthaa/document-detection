from setuptools import setup, find_packages

__version__ = "0.0.1"
AUTHOR = "Saurav Shrestha"
EMAIL = "saurav.shrestha@bitskraft.com"
DESCRIPTION = "Document Detection"

setup(
    name='app',
    author=AUTHOR,
    author_email=EMAIL,
    version=__version__,
    description=DESCRIPTION,
    package_dir={"": "app"},
)
