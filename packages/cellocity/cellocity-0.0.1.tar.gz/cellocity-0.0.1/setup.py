# -*- coding: utf-8 -*-
# Learn more: https://github.com/oftatkofta/cellocity

from setuptools import setup, find_packages


with open('readme.rst') as f:
    readme = f.read()

setup(
    name='cellocity',
    version='0.0.1',
    description='Velocity and vector analysis of microscopy data',
    long_description=readme,
    long_description_content_type='text/x-rst',
    install_requires=["docutils>=0.16"],
    author='Jens Eriksson',
    author_email='jens.eriksson@imbim.uu.se',
    url='https://github.com/oftatkofta/cellocity',
    license="GPLv3",
    packages=find_packages(exclude=('tests', 'docs', '.idea')),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha"
    ],
    python_requires='>=3.6'
    
)