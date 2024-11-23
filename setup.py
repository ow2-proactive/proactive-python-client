from __future__ import print_function
from setuptools import setup, find_packages
import datetime

now = datetime.datetime.now()

with open('VERSION', 'r') as version_file:
    version_content = version_file.read().strip()

with open("README.md", "r") as fh:
    try:
        long_description = fh.read()
    except (OSError, IOError):
        long_description = "Not available"

setup(
    name='proactive',
    version=version_content,
    description='ProActive scheduler client module',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Activeeon',
    author_email='contact@activeeon.com',
    url='https://github.com/ow2-proactive/proactive-python-client',
    license='Apache-2.0',
    test_suite='pytest',
    tests_require=[
        'mock',
        'coverage',
        'coveralls',
        'pytest',
        'python-dateutil',
        'py4j',
        'cloudpickle',
        'codecs'
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
        'requests',
        'py4j',
        'cloudpickle',
        'typer',
        'python-dotenv',
        'wheel',
        'setuptools',
        'humanize'
    ],
    package_dir={'proactive': 'proactive'},
    package_data={'proactive': ['java/lib/*.jar', 'java/log4j.properties', 'logging.conf', '../VERSION']},
    python_requires='>=3.6',
    zip_safe=False
)
