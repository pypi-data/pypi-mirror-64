#!/usr/bin/env python3
# Copyright (C) 2019  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

from setuptools import setup, find_packages

from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()


def parse_requirements(name=None):
    if name:
        reqf = 'requirements-%s.txt' % name
    else:
        reqf = 'requirements.txt'

    requirements = []
    if not path.exists(reqf):
        return requirements

    with open(reqf) as f:
        for line in f.readlines():
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            requirements.append(line)
    return requirements


# Edit this part to match your module.
# Full sample:
#   https://forge.softwareheritage.org/diffusion/DCORE/browse/master/setup.py
setup(
    name='swh.web.client',  # example: swh.loader.pypi
    description='Software Heritage Web client',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    author='Software Heritage developers',
    author_email='swh-devel@inria.fr',
    url='https://forge.softwareheritage.org/source/swh-web-client/',
    packages=find_packages(),  # packages's modules
    install_requires=parse_requirements() + parse_requirements('swh'),
    tests_require=parse_requirements('test'),
    setup_requires=['vcversioner'],
    extras_require={'testing': parse_requirements('test')},
    vcversioner={},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
    ],
    project_urls={
        'Bug Reports': 'https://forge.softwareheritage.org/maniphest',
        'Funding': 'https://www.softwareheritage.org/donate',
        'Source': 'https://forge.softwareheritage.org/source/swh-web-client',
    },
)
