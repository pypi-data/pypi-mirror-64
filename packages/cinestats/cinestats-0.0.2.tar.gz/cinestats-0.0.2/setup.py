from os.path import dirname, join
from setuptools import setup, find_packages


# Parse version information from plain ASCII file.
versionfile = join(dirname(__file__), "cinestats", "VERSION")
__version__ = open(versionfile).read().strip()

# Parse long description from README file.
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="cinestats",
    author="Lukas Kluft",
    author_email="lukas.kluft@gmail.com",
    url="https://github.com/lkluft/cinestats",
    version=__version__,
    packages=find_packages(),
    license="GPL-3.0",
    description="Analyse and visualise statistics around movies and cinema.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Other Audience",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    include_package_data=True,
    python_requires=">=3.6",
    install_requires=[
        "matplotlib",
        "numpy",
    ],
    extras_require={
        "tests": [
            "flake8",
            "pytest",
        ],
    },
)
