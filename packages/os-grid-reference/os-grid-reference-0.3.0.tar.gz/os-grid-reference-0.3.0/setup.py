#!/usr/bin/env python

import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='os-grid-reference',
    version='0.3.0',
    description='Encode and decode British National Grid References',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='JB Robertson',
    author_email='jbr@freeshell.org',
    url='https://gitlab.com/jbrobertson/os-grid-reference',
    packages=['os_grid_reference'],
    python_requires='>=3.6',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ])
