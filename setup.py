import json
from setuptools import setup, find_packages


params = json.load(open("package.json"))


setup(
    name=params["name"],
    version=params["version"],
    description=params["description"],
    long_description=open("README.md", "rt").read(),
    long_description_content_type="text/markdown",
    license=open("LICENSE", "rt").read(),
    zip_safe=False,
    entry_points={"console_scripts": ["emptyfile=emptyfile.__main__:main"]},
    packages=find_packages()
)
