#!/usr/bin/env python2.6

import distribute_setup
distribute_setup.use_setuptools()

from setuptools import setup, find_packages

setup(
    name="NameThatColor",
    version="1.0.1",
    packages=find_packages(),
    entry_points = {
        'console_scripts' : [
            'namethatcolor = NameThatColor:main'
        ]
    },
    scripts = ['namethatcolor/NameThatColor.py'],
    install_requires = ['argparse>=1.1'],
    include_package_data = True,
    author = "Jeremiah Dodds",
    author_email = "jeremiah.dodds@gmail.com",
    description = "Find human-readable color names for hex values",
    long_description=open('README.txt').read(),
    license="LICENSE.txt",
    keywords="color colors webcolor hex css html hue saturation lightness red green blue",
    url="http://github.com/jdodds/py-name-that-color",
    download_url="http://github.com/jdodds/py-name-that-color/downloads",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Topic :: Artistic Software',
        'Topic :: Multimedia',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Printing',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities'
    ]
)
