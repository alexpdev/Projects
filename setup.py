from setuptools import setup, find_packages
import json

INFO = json.load(open('./package.json'))

with open("README.md", encoding="UTF-8") as readme:
    long_description = readme.read()

setup(
    name=INFO['name'],
    version=INFO['version'],
    description=INFO['description'],
    long_description=INFO['long_description'],
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
)
