#!/usr/bin/env python3
import setuptools

setuptools.setup(
    name="micropsi_lines",
    version="0.0.1",
    author="Mia Kokic",
    author_email="mkokic65@gmail.com",
    description="A package for micropsi software test",
    long_description=open('README.md').read(),
    url="https://github.com/pypa/micropsi_lines",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.5',
)
