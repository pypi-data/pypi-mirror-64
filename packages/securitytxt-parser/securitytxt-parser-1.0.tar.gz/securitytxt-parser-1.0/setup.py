# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

try:
    long_description = open("README.rst").read()
except IOError:
    long_description = ""

setup(
    name="securitytxt-parser",
    version="1.0",
    license="MIT",
    author="Tom CHAMBARETAUD",
    author_email="tom.chambaretaud@protonmail.com",
    description="A Python project to parse security.txt file and URL.",
    packages=find_packages(),
    install_requires=["requests"],
    long_description=long_description,
    url="https://github.com/AethliosIK/securitytxt-parser",
    classifiers=[
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
    ]
)
