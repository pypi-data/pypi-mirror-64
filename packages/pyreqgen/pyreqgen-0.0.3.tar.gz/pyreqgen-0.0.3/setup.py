#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='pyreqgen',
      version='0.0.3',
      description='Creates a requirements.txt file for a project '
				  'solely from source files, given a root directory',
      author='Matthew Bladek',
      author_email='malanb5@gmail.com',
	  packages=find_packages(),
	  classifiers=[
		  "Programming Language :: Python :: 3",
		  "License :: OSI Approved :: MIT License",
		  "Operating System :: OS Independent",
	  ],
	  url="https://github.com/malanb5/py_requirements_installer"
     )