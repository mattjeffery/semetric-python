#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright (C) 2013  Matt Jeffery <matt@clan,se>
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA

import os
import sys
from semetric.apiclient import __version__
from setuptools import setup, find_packages

# Utility function to read the README file, etc..
def read(fname):
    fh = None
    try:
        fh = open(os.path.join(os.path.dirname(__file__), fname))
    except:
        if fh:
            fh.close()
        raise
    return fh.read()

if __name__ == "__main__":

    extra = {}
    requirements = read("requirements/requirements.txt").splitlines()

    # unittest2 backport for py3
    if sys.version_info >= (3,):
        extra['use_2to3'] = True
        pkg_unittest2 = 'unittest2py3k'
    else:
        pkg_unittest2 = 'unittest2'

    # Python 2 extra requirements
    if sys.version_info < (3,):
        requirements.append(read("requirements/requirements_py2.txt").splitlines())

    # Python 3 extra requirements
    if sys.version_info >= (3,):
        requirements.append(read("requirements/requirements_py3.txt").splitlines())

    setup(
        name="semetric.apiclient",
        version=__version__,
        author="Matt Jeffery",
        author_email="matt@clan.se",
        # read the install requirements from the requirements.txt
        install_requires=requirements,
        description=("Wrapper for the Semetric API"),
        long_description=read('README.rst'),
        url="http://developer.musicmetric.com",
        license="LGPLv2+",
        namespace_packages=['semetric'],
        packages=find_packages(exclude=['tests']),
        include_package_data=True,
        test_suite='nose.collector',
        tests_require=['nose>=1.3.0',
                       'mock',
                       pkg_unittest2],
        zip_safe=False,
        platforms='any',
        classifiers=[
            "Development Status :: 3 - Alpha",
            "Framework :: Setuptools Plugin",
            "Intended Audience :: Developers",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.6",
            "Programming Language :: Python :: 2.7",
            "Programming Language :: Python :: 3.2",
            "Programming Language :: Python :: 3.3",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        ],
        entry_points = {'console_scripts': [
                'semetric-api = semetric.apiclient:main',
            ],
        },
        **extra
    )
