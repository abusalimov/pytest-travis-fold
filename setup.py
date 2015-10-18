#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-travis-fold',
    version='1.0.0',
    author='Eldar Abusalimov',
    author_email='eldar.abusalimov@gmail.com',
    maintainer='Eldar Abusalimov',
    maintainer_email='eldar.abusalimov@gmail.com',
    license='MIT',
    url='https://github.com/abusalimov/pytest-travis-fold',
    description='Folds captured output sections in Travis CI build log',
    long_description=read('README.rst'),
    py_modules=['pytest_travis_fold'],
    install_requires=['pytest>=2.6.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    keywords='pytest travis build logs continuous integration',
    entry_points={
        'pytest11': [
            'travis-fold = pytest_travis_fold',
        ],
    },
)
