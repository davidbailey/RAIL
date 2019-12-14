#!/usr/bin/env python

from setuptools import setup

setup(
    name="RAIL",
    version="0.6",
    description="Risk Assessment Library",
    author="David Bailey",
    author_email="david@davidabailey.com",
    url="https://github.com/davidbailey/rail",
    packages=["rail"],
    license="MIT License",
    install_requires=["matplotlib", "numpy", "pandas", "scipy"],
    tests_requires=["black", "coveralls", "pytest", "pytest-cov"],
)
