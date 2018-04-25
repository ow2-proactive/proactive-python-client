from __future__ import print_function
import os
import sys
import time
import pkg_resources
import platform
from setuptools import setup, find_packages, Command
from setuptools.command.install_egg_info import install_egg_info as _install_egg_info
from setuptools.dist import Distribution

gradle_properties={}
with open('gradle.properties') as fp:
  for line in fp:
    if '=' in line:
      name, value = line.replace('\n','').split('=', 1)
      if "SNAPSHOT" in value:
          dev_version = ".dev" + str(int(time.time()))
          value = value.replace("-SNAPSHOT", dev_version)              
          
      gradle_properties[name] = value
      
  
setup(
  name='proactive',
#  version=gradle_properties['version'],
  version=gradle_properties["version"],
  description='ProActive scheduler client module',
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
    'py4j'
  ],
  package_dir={'proactive': 'proactive'},
  package_data={'proactive': ['java/lib/*.jar']},
  python_requires='>=3',
  zip_safe=False
)
