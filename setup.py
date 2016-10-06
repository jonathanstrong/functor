#!/usr/bin/env python

# Bootstrap installation of Distribute
import distribute_setup
distribute_setup.use_setuptools()

import os

from setuptools import setup


PROJECT = u'Functor'
VERSION = '0.1'
URL = ''
AUTHOR = u'Jonathan Strong'
AUTHOR_EMAIL = u'jonathan.strong@gmail.com'
DESC = "Implements a function-object pattern in Python."

def read_file(file_name):
    file_path = os.path.join(
        os.path.dirname(__file__),
        file_name
        )
    return open(file_path).read()

setup(
    name=PROJECT,
    version=VERSION,
    description=DESC,
    long_description=read_file('README.md'),
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    license=read_file('LICENSE'),
    namespace_packages=[],
    packages=[u'functor'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Requirements -*-
    ],
    entry_points = {
        # -*- Entry points -*-
    },
    classifiers=[
    	# see http://pypi.python.org/pypi?:action=list_classifiers
        # -*- Classifiers -*-
        "Programming Language :: Python",
    ],
)
