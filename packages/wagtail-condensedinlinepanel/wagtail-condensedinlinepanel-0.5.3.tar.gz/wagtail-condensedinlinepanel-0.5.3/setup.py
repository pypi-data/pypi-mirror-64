#!/usr/bin/env python

import sys
import pathlib

from setuptools import setup, find_packages


from condensedinlinepanel import __version__

from setuptools import setup, find_packages

setup(
    name='wagtail-condensedinlinepanel',
    version=__version__,
    description='',
    author='Karl Hobley',
    author_email='karl@kaed.uk',
    url='https://github.com/wagtail/wagtail-condensedinlinepanel',
    packages=find_packages(),
    include_package_data=True,
    license='BSD',
    long_description=pathlib.Path('./README.md').read_text(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Wagtail',
        'Framework :: Wagtail :: 2',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
    ],
    install_requires=[],
    zip_safe=False,
)
