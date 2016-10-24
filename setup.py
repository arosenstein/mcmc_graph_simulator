#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='mcmc_graph_simulator',
    version='0.1.0',
    description="A Markov-Chain Monte Carlo simulator for cevaluating graphs using python.",
    long_description=readme + '\n\n' + history,
    author="Adam Rosenstein",
    author_email='adamrosenstein19@gmail.com',
    url='https://github.com/arosenstein/mcmc_graph_simulator',
    packages=[
        'mcmc_graph_simulator',
    ],
    package_dir={'mcmc_graph_simulator':
                 'mcmc_graph_simulator'},
    entry_points={
        'console_scripts': [
            'mcmc_graph_simulator=mcmc_graph_simulator.cli:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='mcmc_graph_simulator',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
