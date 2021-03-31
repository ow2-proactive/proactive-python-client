from __future__ import print_function
from setuptools import setup, find_packages
import datetime

now = datetime.datetime.now()

gradle_properties = {}
with open('gradle.properties') as fp:
    for line in fp:
        if '=' in line:
            name, value = line.replace('\n', '').split('=', 1)
            if "SNAPSHOT" in value:
                dev_version = "." + now.strftime("%y%m%d%H%M") + "dev"
                # dev_version = "." + now.strftime("%y%m%d%H%M")
                value = value.replace("-SNAPSHOT", dev_version)
            gradle_properties[name] = value

with open("README.md", "r") as fh:
    try:
        long_description = fh.read()
    except (OSError, IOError):
        long_description = "Not available"

setup(
    name='proactive',
    version=gradle_properties["version"],
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
        'cloudpickle'
    ],
    package_dir={'proactive': 'proactive'},
    package_data={'proactive': ['java/lib/*.jar', 'java/log4j.properties', 'logging.conf']},
    python_requires='>=2.7',
    zip_safe=False
)
