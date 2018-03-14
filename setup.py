# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='proactive-client',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='Kenneth Reitz',
    author_email='me@kennethreitz.com',
    url='https://github.com/ow2-proactive/client-python',
    license=license,
    test_suite='pytest',
    tests_require=[
          'mock',
          'coverage',
          'coveralls',
          'pytest',
          'python-dateutil'
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
          'requests'
      ],
    zip_safe=False
)

