#!/usr/bin/env python
# -*- coding:utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="sppush",
    version="1.0.4",
    keywords=("sppush",),
    description="sdk for sppush",
    long_description="sdk for sppush",
    license="MIT",
    url="https://github.com/baidu-spp/spp-sdk-python",
    author="baidu-sppush",
    author_email="liangjunyu@baidu.com",
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=["requests", "six"]
)
