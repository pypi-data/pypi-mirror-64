#!/usr/bin/python3
# coding: utf-8
import os
import sys
from setuptools import setup
from setuptools.command.install import install

try:
    from pypandoc import convert

    read_md = lambda f: convert(f, "rst")
except ImportError:
    print("warning: pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, "r").read()

VERSION = "3.1.0"


class VerifyVersionCommand(install):
    description = "verify that the git tag matches our version"

    def run(self):
        tag = os.getenv("CIRCLE_TAG")
        if tag != VERSION:
            info = "Git tag: {0} does not match the version of this app: {1}".format(
                tag, VERSION
            )
            sys.exit(info)


setup(
    name="pycti",
    version=VERSION,
    description="Python API client for OpenCTI.",
    long_description="Official Python client for the OpenCTI platform.",
    author="OpenCTI",
    author_email="contact@opencti.io",
    maintainer="OpenCTI",
    url="https://github.com/OpenCTI-Platform/client-python",
    license="Apache",
    packages=["pycti", "pycti.api", "pycti.connector", "pycti.entities", "pycti.utils"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Natural Language :: French",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    include_package_data=True,
    install_requires=[
        "requests",
        "PyYAML",
        "python-dateutil",
        "datefinder",
        "stix2",
        "stix2-validator",
        "pytz",
        "pika",
        "deprecated",
        "python-magic",
    ],
    cmdclass={"verify": VerifyVersionCommand,},
    extras_require={"dev": ["black", "wheel"],},  # Optional
)
