# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wikirevparser",
    version="0.0.2",
    author="Anna Jørgensen",
    author_email="anka.jorgensen@gmail.com",
    description="Wikipedia revision history parser for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajoer/WikiRevisionParser",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
