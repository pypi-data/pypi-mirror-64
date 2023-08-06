#!/usr/bin/env python

import setuptools
import os

# Install Requirements from requirements.txt
thelibFolder = os.path.dirname(os.path.realpath(__file__))
requirementPath = thelibFolder + '/requirements/dev.txt'
install_requires = [] 
if os.path.isfile(requirementPath):
    with open(requirementPath) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dosk", # Replace with your own username
    version="0.0.5",
    author="Richard Wolf",
    author_email="richard.wolf@stelligent.com",
    description="DevOps Task Runner",
    url="https://github.com/stelligent/dosk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=install_requires,
    scripts=['bin/dosk_cli.py'],
#    entry_points ={ 
#            'console_scripts': [ 
#                'dosk = dosk.command_line:main'
#            ] 
#        }
)
