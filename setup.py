# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from rockload.version import __version__

setup(
    name='rockload',
    version=__version__,
    description="rockload is a load testing tool that keeps track of how your projects evolve.",
    long_description="rockload is a load testing tool that keeps track of how your projects evolve.",
    keywords='load testing benchmark funkload',
    author='Bernardo Heynemann',
    author_email='heynemann@gmail.com',
    url='http://heynemann.github.com/rockload',
    license='MIT',
    classifiers=['Development Status :: 3 - Alpha',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: MIT License',
                 'Natural Language :: English',
                 'Operating System :: MacOS',
                 'Operating System :: Microsoft :: Windows',
                 'Operating System :: POSIX :: Linux',
                 'Programming Language :: Python :: 2.6',
                 'Topic :: System :: Installation/Setup'
    ],
    packages=find_packages(),
    include_package_data=True,
    package_data={
    },

    install_requires=[
        "tornado==2.0.0",
        "aero==0.3.3a",
        "mongoengine==0.4.0",
        "funkload==1.16.1",
        "fabric==1.2.0",
        "lxml==2.2.8"
    ],

    entry_points={
        'console_scripts': [
            'rockload-server = rockload.server:main',
            'rockload-cli = rockload-client.cli:main',
        ],
    },

)
