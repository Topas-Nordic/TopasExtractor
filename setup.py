#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(name='tpextract',
      version='1.0',
      description='A python package for extracting Topas parameters from .OUT files.',
      url='https://github.uio.no/IN3110/IN3110-nicolhaa/tree/master/assignment4/instapy-git',
      author='Nicolai Haaber Junge',
      author_email='n.h.junge@smn.uio.no',
      license='MIT',
      entry_points={
        'console_scripts': [
            'tpextract=bin.tpextract:main',
        ]
      },
      include_package_data=True,
      packages=find_packages(),
      install_requires=['pandas'],
      python_requires='>=3.8'
    )