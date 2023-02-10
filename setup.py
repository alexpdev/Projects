<<<<<<< HEAD
#! /usr/bin/python3
# -*- coding: utf-8 -*-

#############################################################################
# Copyright (C) 2021 alexpdev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################

from setuptools import setup, find_packages
import json

INFO = json.load(open('./package.json'))

def readme():
    with open("README.md", encoding="UTF-8") as fd:
        long_description = fd.read()
    return long_description

setup(
    name=INFO['name'],
    version=INFO['version'],
    description=INFO['description'],
    long_description=readme(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
    ],
    keywords=INFO["keywords"],
    author=INFO["author"],
    author_email=INFO["email"],
    url=INFO["url"],
    project_urls={"Source Code": "https://github.com/alexpdev/tempath"},
    license=INFO["license"],
    packages=find_packages(exclude=["env","tests"]),
    include_package_data=True,
    tests_require=['pytest'],
    setup_requires=["setuptools", 'wheel'],
    zip_safe=False,
    test_suite='complete',
)
#! /usr/bin/python3
# -*- coding: utf-8 -*-

<<<<<<< HEAD
#############################################################################
# MinMaxPlus  extends builtin min and max functions.
# Copyright (C) 2021 alexpdev
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
############################################################################


from setuptools import setup, find_packages
import json

INFO = json.load(open('./package.json'))

with open("README.md", encoding="UTF-8") as readme:
    long_description = readme.read()

setup(
    name=INFO['name'],
    version=INFO['version'],
    description=INFO['description'],
    long_description=long_description,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
"""Setup for Torrentfile package."""

import json

from setuptools import find_packages, setup


def load_info():
    """Extract information from package.json."""
    return json.load(open("package.json"))


def load_description():
    """Load readme into long description parameter."""
    with open("README.md", "rt", encoding="utf-8") as readme:
        long_description = readme.read()
    return long_description


INFO = load_info()

setup(
    name=INFO["name"],
    version=INFO["version"],
    description=INFO["description"],
    long_description=load_description(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU Lesser General Public License v3"
        " (LGPLv3)",
    ],
    keywords=INFO["keywords"],
    author=INFO["author"],
    author_email=INFO["email"],
    url=INFO["url"],
    project_urls={"Source Code": "https://github.com/alexpdev/MinMaxObj"},
    license=INFO["license"],
    packages=find_packages(exclude=["tests", "env"]),
    include_package_data=True,
    install_requires=[],
    tests_require=["pytest"],
    setup_requires=["setuptools"],
    zip_safe=False,
    test_suite="complete",
from setuptools import setup

setup(
    name="bitprint",
    version="0.1.0",
    author="alexpdev",
    author_email="alexpdev@protonmail.com",
    packages=["bitprint"],
    entry_points={"console_scripts":["bitprint = bitprint:execute"]},
    description="convert integers to binary",
    project_urls={"Source Code": "https://github.com/alexpdev/torrentfile"},
    license=INFO["license"],
    packages=find_packages(exclude=["env", "tests"]),
    include_package_data=True,
    entry_points={"console_scripts": ["torrentfile = torrentfile.cli:main"]},
    tests_require=["pytest"],
    install_requires=["pyben", "tqdm"],
    zip_safe=False,
    test_suite="complete",
)
=======
##############################################################################
#    Copyright (C) 2021-current alexpdev
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
##############################################################################
"""Setup Module."""

from setuptools import setup

setup()
>>>>>>> 82330a7980332da35d5c1048959db71f75cccaf6
=======
import os
import json
from setuptools import setup, find_packages

pkg = os.path.join(os.path.dirname(os.path.abspath(__file__)), "package.json")
params = json.load(open(pkg))

setup(
    name=params["name"],
    version=params["version"],
    description=params["description"],
    license=open("LICENSE", "rt").read(),
    zip_safe=False,
    entry_points={"console_scripts": ["emptyfile=emptyfile.__main__:main"]},
    packages=find_packages(),
    requires=(),
    include_package_data=True
)
>>>>>>> 847257796971bda380b5d2930f772bde3c84d257
