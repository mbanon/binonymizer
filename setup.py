#!/usr/bin/env python

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
with open("requirements.txt") as rf:
    requirements = rf.read().splitlines()

setuptools.setup(
    name="binonymizer",
    version="0.1.1",
    install_requires=requirements,
    license="GNU General Public License v3.0",
    author="Prompsit Language Engineering",
    author_email="info@prompsit.com",
    maintainer="Marta Bañón",
    maintainer_email="mbanon@prompsit.com",
    description="Binonymizer is a tool in Python that aims at tagging personal data in a parallel corpus.",
    long_description=long_description,
    long_description_content_type="text/markdown",    
    url="https://github.com/bitextor/binonymizer",
    packages=setuptools.find_packages(),    
    classifiers=[
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Filters"
    ],
    project_urls={
        "Binonymizer on GitHub": "https://github.com/bitextor/binonymizer",
        "Prompsit Language Engineering": "http://www.prompsit.com",
        "Paracrawl": "https://paracrawl.eu/"
         },
    scripts=[
         "scripts/binonymizer",
         "scripts/binonymizer-lite"
         ]
)



