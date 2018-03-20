#
# Copyright 2016 LinkedIn Corp.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import os
import sys
import pkg_resources
import platform
import jprops

from setuptools import setup, find_packages, Command
from setuptools.command.install_egg_info import install_egg_info as _install_egg_info
from setuptools.dist import Distribution




with open('gradle.properties') as fp:
  gralde_properties = jprops.load_properties(fp)
  
  
setup(
    name='proactive',
    version=gralde_properties['version'],
    description='ProActicve scheduler client module',
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
          'python-dateutil',
          'py4j'
    ],
    packages=find_packages(exclude=('tests', 'docs')),
    install_requires=[
          'requests',
          'py4j'
      ],
    package_dir={'proactive': 'proactive'},
    package_data={'proactive': ['java/lib/*.jar']},
    zip_safe=False
)

