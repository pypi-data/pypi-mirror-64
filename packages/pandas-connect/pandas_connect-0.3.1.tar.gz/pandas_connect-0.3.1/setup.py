#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

setup(
    author="Eric Hamers",
    author_email='erichamers@gmail.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Pandas connection methods for multiple databases. SQL and NoSQL.",
    entry_points={
        'console_scripts': [
            'pandas_connect=pandas_connect.cli:main',
        ],
    },
    install_requires=[
        "pandas"
    ],
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pandas_connect',
    name='pandas_connect',
    packages=find_packages(include=['pandas_connect', 'pandas_connect.*']),
    test_suite='tests',
    url='https://github.com/erichamers/pandas_connect',
    version='0.3.1',
    zip_safe=False,
)
