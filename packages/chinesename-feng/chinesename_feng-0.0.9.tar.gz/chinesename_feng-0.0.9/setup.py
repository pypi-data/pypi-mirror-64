#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2020 NetEase.com, Inc. All Rights Reserved.
# Copyright 2020, The Fuxi AI Lab.
"""
desc

Authors: fengxiaochuan(fengxiaochuan@corp.netease.com)
Phone: 15664601006
Date: 2020/3/24

"""
import io

import setuptools
import os
import requests


# 将markdown格式转换为rst格式
def md_to_rst(from_file, to_file):
    r = requests.post(url='http://c.docverter.com/convert',
                      data={'to':'rst','from':'markdown'},
                      files={'input_files[]':open(from_file,'rb')})
    if r.ok:
        with open(to_file, "wb") as f:
            f.write(r.content)


md_to_rst("README.md", "README.rst")

if os.path.exists('README.rst'):
    long_description = open('README.rst', encoding="utf-8").read()
else:
    long_description = 'Add a fallback short description here'

if os.path.exists("requirements.txt"):
    install_requires = io.open("requirements.txt").read().split("\n")
else:
    install_requires = []

setuptools.setup(
    name="chinesename_feng",
    version="0.0.9",
    author="fengxiaochuan",
    author_email="fengxiaochuan@corp.netease.com",
    license='MIT License',
    url="https://github.com/mouday/chinesename",
    packages=setuptools.find_packages(),
    description='get a chinesename by random',
    install_requires=install_requires,
)
