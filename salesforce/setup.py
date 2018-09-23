#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name='demo-salesforce',
    version='0.0.1',
    description='Demo salesforce service',
    packages=find_packages("src"),
    package_dir={},
    install_requires=[
        "nameko==2.9.0-rc0",
        "nameko-salesforce==1.2.0",
        "nameko-amqp-retry==0.6.0",
        "nameko-tracer==1.2.0",
        "nameko-slack==0.0.5",
        "nameko-redis-1.1.0",
        "ddebounce==0.0.1",  # TODO
    ],
    extras_require={
        'dev': [
        ],
    },
    zip_safe=True
)
