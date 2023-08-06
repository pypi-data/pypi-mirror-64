from setuptools import setup, find_namespace_packages

setup(
    name='adventofcode.utils',
    version='1.0',
    description='Advent of Code utility classes',
    author='David Hanley',
    author_email='hanley_d@hotmail.com',
    package_dir={"": "src"},
    packages=find_namespace_packages(where="src")
)