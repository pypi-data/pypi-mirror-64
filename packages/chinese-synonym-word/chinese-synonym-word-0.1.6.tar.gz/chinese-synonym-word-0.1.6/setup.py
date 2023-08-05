#!/usr/bin/env python
# -*- coding:utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chinese-synonym-word",
    version="0.1.6",
    author="sunsi",
    author_email="449860952@qq.com",
    description="chinese-synonym-word",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Suncicie/chinese-synonym-word",
    license='MIT',
    packages=["chinese_synonym_word"], # 包名，二级目录
    package_dir={"chinese_synonym_word": "chinese_synonym_word"}, # ？映射关系好像
    package_data={"": ["*.model"],
                  'chinese_synonym_word': ['model/*']}, # 包名下对应的数据
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)


