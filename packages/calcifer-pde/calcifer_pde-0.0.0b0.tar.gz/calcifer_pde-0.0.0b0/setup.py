#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

REQUIRES = [
    "numpy",
    "scipy",
    'PyYAML',
    "arnica"
]

setup(
    name='calcifer_pde',
    version='0.0.0b',
    description='Template module description',
    long_description=readme,
    author='COOP',
    author_email='coop@cerfacs.fr',
    url='https://nitrox.cerfacs.fr/open-source/calcifer',
    license=license,
    packages=find_packages(exclude=('tests', 'docs')),
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    install_requires=REQUIRES
)

