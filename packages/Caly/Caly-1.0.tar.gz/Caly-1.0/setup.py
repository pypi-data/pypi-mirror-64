#!/usr/bin/env python
'''
 @package   caly
 @file      setup.py
 @brief     Install caly
 @copyright GPLv3
 @author    Yves Revaz <yves.revaz@epfl.ch>
 @section   COPYRIGHT  Copyright (C) 2020 EPFL (Ecole Polytechnique Federale de Lausanne)  LASTRO - Laboratory of Astrophysics of EPFL

 This file is part of caly.
'''

from setuptools import setup, find_packages
from glob import glob


# scripts to install
scripts = glob("scripts/caly")
data = [("conf/txt", glob("conf/txt/*")),("conf/sounds", glob("conf/sounds/*"))]

setup(
    name="Caly",
    author="Yves Revaz",
    author_email="yves.revaz@epfl.ch",
    url="http://obswww.unige.ch/~revaz",
    description="""caly module""",
    license="GPLv3",
    version="1.0",

    packages=find_packages(),
    scripts=scripts,
    install_requires=["numpy","pyQt5"],    
    data_files=data
)
