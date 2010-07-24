#!/usr/bin/env python

import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name="NameThatColor",
    version="1.0",
    packages=find_packages('src'),
    package_dir = {'':'src'},
    entry_points = {
        'console_scripts' : [
            'namethatcolor = NameThatColor:main'
        ]
    },
    scripts = ['src/NameThatColor.py'],
    install_requires = ['argparse>=1.1'],
    package_data = {
        'data': 'colors.csv'
    },
    author = "Jeremiah Dodds",
    author_email = "jeremiah.dodds@gmail.com",
    description = "Find human-readable color names for hex values",
    license="BSD",
    keywords="color colors webcolor hex css html hue saturation lightness red green blue",
    url="http://github.com/jdodds/py-name-that-color",
    download_url="http://github.com/downloads/jdodds/py-name-that-color/NameThatColor-1.0.tar.gz",
    zip_safe=True,
)
