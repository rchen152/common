"""Setup file."""

import os
from setuptools import find_packages, setup

_VERSION = '0.5.3'


def get_long_description():
    with open(os.path.join(os.path.dirname(__file__), 'README.md'), 'r') as f:
        return f.read()


setup(
    name='kitty-common',
    version=_VERSION,
    description='kitty games common library',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    url='https://github.com/rchen152/common',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=True,
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
    ],
    python_requires='>=3.6',
    install_requires=['pygame'],
)
