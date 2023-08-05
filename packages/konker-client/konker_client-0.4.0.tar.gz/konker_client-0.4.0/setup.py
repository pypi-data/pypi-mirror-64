#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['paho-mqtt', 'psutil', 'netifaces', 'aiohttp']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Gustavo Esteves de Andrade",
    author_email='gandrade@inmetrics.com.br',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    description="Konker Client to easier send and receive messages in the plataform via MQTT and Request",
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='konker_client',
    name='konker_client',
    packages=find_packages(include=['konker_client']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/gandrade/konker_client',
    version='0.4.0',
    zip_safe=False,
)
