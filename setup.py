# -*- coding: utf-8 -*-

# Learn more: https://github.com/kennethreitz/setup.py

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='scheduler_client',
    version='0.1.0',
    description='ProActicve scheduler client module',
    long_description=readme,
    author='Activeeon',
    author_email='info@activeeon.com',
    url='https://github.com/ow2-proactive/proactive-python-client',
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

