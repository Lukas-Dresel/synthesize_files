from setuptools import setup
from setuptools import find_packages
from distutils.command.build import build as _build #pylint:disable=no-name-in-module,import-error
from setuptools.command.develop import develop as _develop
packages = find_packages()

import subprocess
import os

#if bytes is str:
#    raise Exception("This module is designed for python 3 only.")


setup(
    name='synthesize_files',
    version='0.0.0.1',
    python_requires='>=2.7',
    packages=packages,
    install_requires=[
        'bitstring',
    ],
    description='Scripts to easily synthesize file formats',
    url='https://github.com/Lukas-Dresel/synthesize_files',
)
