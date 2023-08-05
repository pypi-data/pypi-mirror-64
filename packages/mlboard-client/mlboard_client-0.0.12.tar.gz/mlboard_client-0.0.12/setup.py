#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

requires = [
    "requests",
]

dev_requires = [
    "pytest",
    "pytest-cov",
    "flake8",
    "autopep8",
    "mypy",
    "black",
    "pytest-mypy",
    "twine",
]

setup(
    name="mlboard_client",
    version="0.0.12",
    description="mlboard client",
    author="Xinyuan Yao",
    author_email="yao.ntno@google.com",
    license="MIT",
    packages=["mlboard_client"],
    package_data={"mlboard_client": ["py.typed"],},
    install_requires=requires,
    extras_require={"dev": dev_requires},
    python_requires=">=3.6",
)
