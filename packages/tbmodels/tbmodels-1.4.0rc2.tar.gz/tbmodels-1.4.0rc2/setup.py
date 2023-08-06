#!/usr/bin/env python
# -*- coding: utf-8 -*-

# (c) 2015-2018, ETH Zurich, Institut fuer Theoretische Physik
# Author: Dominik Gresch <greschd@gmx.ch>

import re
from setuptools import setup, find_packages

import sys

if sys.version_info < (3, 6):
    raise ValueError("must use Python version 3.6 or higher")

with open("./README.md", "r") as f:
    README = f.read()

with open("./tbmodels/__init__.py", "r") as f:
    MATCH_EXPR = "__version__[^'\"]+(['\"])([^'\"]+)"
    VERSION = re.search(MATCH_EXPR, f.read()).group(2).strip()  # type: ignore

EXTRAS_REQUIRE = {
    "kwant": ["kwant"],
    "dev": [
        "pytest",
        "pytest-cov",
        "pythtb",
        "sphinx",
        "sphinx-rtd-theme",
        "ipython>=7.10",
        "sphinx-click",
        "black==19.10b0",
        "pre-commit",
        "prospector==1.2.0",
        "pylint==2.4.4",
        "mypy==0.770",
    ],
}
EXTRAS_REQUIRE["dev"] += EXTRAS_REQUIRE["kwant"]

setup(
    name="tbmodels",
    version=VERSION,
    url="http://tbmodels.greschd.ch",
    author="Dominik Gresch",
    author_email="greschd@gmx.ch",
    description="A tool for reading, creating and modifying tight-binding models.",
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "scipy>=0.14",
        "h5py",
        "fsc.export",
        "symmetry-representation>=0.2",
        "click>=7.0, !=7.1.0",
        "bands-inspect",
        "fsc.hdf5-io>=0.6.0",
    ],
    extras_require=EXTRAS_REQUIRE,
    long_description=README,
    long_description_content_type="text/markdown",
    classifiers=[  # yapf:disable
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    entry_points={
        "console_scripts": ["tbmodels = tbmodels._cli:cli"],
        "fsc.hdf5_io.load": ["tbmodels = tbmodels"],
    },
    license="Apache 2.0",
    packages=find_packages(),
    package_data={"tbmodels": ["py.typed"],},
)
