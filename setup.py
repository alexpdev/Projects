from setuptools import setup

setup(
    name="bitprint",
    version="0.1.0",
    author="alexpdev",
    author_email="alexpdev@protonmail.com",
    packages=["bitprint"],
    entry_points={"console_scripts":["bitprint = bitprint:execute"]},
    description="convert integers to binary",
)
