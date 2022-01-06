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
from setuptools import setup



setup(
    name="shacffi",
    version="0.0.1",
    description="Python C Lib SHA",
    long_description="A C library ported to python language.",
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU Lesser General Public License v3"
        " (LGPLv3)",
    ],
    keywords=["hashing"],
    author="alexpdev",
    author_email="alexpdev@protonmail.com",
    url="https://github.com/alexpdev/shacffi",
    project_urls={"Source Code": "https://github.com/alexpdev/shacffi"},
    license=open("LICENSE","rt").read(),
    packages=["src", "modules"],
    include_package_data=True,
    install_requires=["cffi"],
    setup_requires=["cffi"],
    zip_safe=False,
)
