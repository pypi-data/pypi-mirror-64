#!/usr/bin/env python

from setuptools import setup, find_packages
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(name='pyreqgen',
      version='0.0.4',
      description='Creates a requirements.txt file for a project '
				  'solely from source files, given a root directory',
      author='Matthew Bladek',
      author_email='malanb5@gmail.com',
	  packages=find_packages(),
      long_description=long_description,
      long_description_content_type='text/markdown',
	  classifiers=[
		  "Programming Language :: Python :: 3",
		  "License :: OSI Approved :: MIT License",
		  "Operating System :: OS Independent",
	  ],
	  url="https://github.com/malanb5/py_requirements_installer"
     )
