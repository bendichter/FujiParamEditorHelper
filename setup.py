#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='FujiParamEditorHelper',
      version='0.1',
      description='Interface with FujiParamEditor',
      author='Ben Dichter',
      author_email='ben.dichter@gmail.com',
      url='',
      packages=find_packages(),
      install_requires=['pandas','numpy']
     )