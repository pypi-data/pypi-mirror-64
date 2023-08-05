#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='puncurl',
    version='0.0.12',
    description='A library to convert curl requests to python-requests.',
    author='Fernanda Panca Prima',
    author_email='pancaprima8@gmail.com',
    url='https://github.com/pancaprima/uncurl',
    entry_points={
        'console_scripts': [
            'uncurl = uncurl.bin:main',
        ],
    },
    install_requires=['xerox', 'six'],
    packages=find_packages(exclude=("tests", "tests.*")),
)
