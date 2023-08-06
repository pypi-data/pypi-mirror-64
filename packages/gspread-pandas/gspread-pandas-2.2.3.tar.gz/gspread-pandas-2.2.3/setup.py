from codecs import open
from os import path

from setuptools import find_packages, setup

__version__ = "version read in next line"
exec(open("gspread_pandas/_version.py").read())

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

# get the dependencies and installs
with open(path.join(here, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [
    x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")
]

# get the dependencies and installs
with open(path.join(here, "requirements_dev.txt"), encoding="utf-8") as f:
    dev_requires = f.read().split("\n")

setup(
    name="gspread-pandas",
    version=__version__,
    description=(
        "A package to easily open an instance of a Google spreadsheet and "
        "interact with worksheets through Pandas DataFrames."
    ),
    long_description=long_description,
    url="https://github.com/aiguofer/gspread-pandas",
    download_url="https://github.com/aiguofer/gspread-pandas/tarball/v" + __version__,
    license="BSD",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
    ],
    keywords="gspread pandas google spreadsheets",
    packages=find_packages(exclude=["docs", "tests*"]),
    include_package_data=True,
    author="Diego Fernandez",
    install_requires=install_requires,
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    extras_require={"dev": dev_requires},
    dependency_links=dependency_links,
    author_email="aiguo.fernandez@gmail.com",
)
