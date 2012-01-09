# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from rockload.version import __version__

setup(
    name='rockload',
    version='.'.join([str(item) for item in __version__]),
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
    packages=find_packages(exclude=['vows']),
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        "tornado==2.0.0",
        "aero==0.3.6a",
        "mongoengine==0.4.0",
        "funkload==1.16.1",
        "fabric==1.3.3",
        "lxml"
    ],

    entry_points={
        'console_scripts': [
            'rockload-server = rockload.server:main',
            'rockload-cli = rockload_client.cli:main',
        ],
    },

)
