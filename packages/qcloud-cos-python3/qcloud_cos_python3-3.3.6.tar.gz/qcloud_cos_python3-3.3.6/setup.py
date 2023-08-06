#!/usr/bin/env python3
# coding=utf-8

import sys
if sys.version_info[0] != 3:
    sys.exit('Sorry, only python3 is supported')

from setuptools import setup, find_packages
setup(
        name = 'qcloud_cos_python3',
        version = '3.3.6',
        description = 'python sdk for tencent qcloud cos',
        license = 'MIT License',
        install_requires=['requests'],

        author = 'songjian',
        author_email = 'jian.song@nexttao.com',

        packages = find_packages(),
        python_requires='>=3.7',
        )
