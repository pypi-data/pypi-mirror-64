# -*- coding: utf-8 -*-
# Copyright (C) 2020 HE Yaowen <he.yaowen@hotmail.com>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='aliros',
    version='0.0.1',
    author='HE Yaowen',
    author_email='he.yaowen@hotmail.com',
    description='This package provides a command-line interface to Resource Orchestration Service for Alibaba Cloud.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/he-yaowen/aliros',
    packages=setuptools.find_packages(),
    install_requires=[
        'aliyun-python-sdk-core==2.13.15',
        'aliyun-python-sdk-ros==3.2.0',
        'jmespath==0.9.5',
        'pycryptodome==3.9.7',
        'PyYAML==5.3.1'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent'
    ],
    entry_points={
        'console_scripts': ['aliros=aliros.__main__:main']
    }
)
