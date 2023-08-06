#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('requirements_dev.txt') as f:
    requirements = f.read().splitlines()

setup_requirements = [ ]

test_requirements = [ ]

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
'alabaster',
'appdirs',
'argh',
'Babel',
'bleach',
'bump2version',
'certifi',
'chardet',
'Click',
'coverage',
'distlib',
'docutils',
'entrypoints',
'filelock',
'flake8',
'idna',
'imagesize',
'importlib-metadata',
'importlib-resources',
'Jinja2',
'MarkupSafe',
'mccabe',
'numpy',
'packaging',
'pandas',
'pathtools',
'pkg-resources',
'pkginfo',
'pluggy',
'psycopg2-binary',
'py',
'pycodestyle',
'pyflakes',
'Pygments',
'pymongo',
'PyMySQL',
'pyparsing',
'python-dateutil',
'pytz',
'PyYAML',
'readme-renderer',
'requests',
'requests-toolbelt',
'six',
'snowballstemmer',
'Sphinx',
'sphinxcontrib-websupport',
'toml',
'tox',
'tqdm',
'twine',
'urllib3',
'virtualenv',
'watchdog',
'webencodings',
'zipp'
    ],
    license="Apache Software License 2.0",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='pandas_connect',
    name='pandas_connect',
    packages=find_packages(include=['pandas_connect', 'pandas_connect.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/erichamers/pandas_connect',
    version='0.3.0',
    zip_safe=False,
)
