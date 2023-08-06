#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'chibi-requests>=0.3.3', 'PyPDF2>=1.26.0', 'camelot-py[cv]>=0.7.3'
]

setup(
    author="dem4ply",
    author_email='dem4ply@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: Public Domain',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="corona chan scraper for gob mx",
    entry_points={
        'console_scripts': [
            'corona_chan_gob_mx=corona_chan_gob_mx.cli:main',
        ],
    },
    install_requires=requirements,
    license="WTFPL",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='corona_chan_gob_mx',
    name='corona_chan_gob_mx',
    packages=find_packages(include=['corona_chan_gob_mx', 'corona_chan_gob_mx.*']),
    url='https://github.com/dem4ply/corona_chan_gob_mx',
    version='1.0.0',
    zip_safe=False,
)
