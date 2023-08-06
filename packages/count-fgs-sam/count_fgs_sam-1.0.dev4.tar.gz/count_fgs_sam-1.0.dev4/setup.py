#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="count_fgs_sam",
    version="1.0.dev4",
    author="Tet Woo Lee",
    author_email="developer@twlee.nz",
    description="Count Functional Genomics Screen alignments in a SAM/BAM file with filtering options",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/twlee79/count_fgs_sam",
    packages=setuptools.find_packages(),
    package_data={'count_fgs_sam.tests': ['output*.tsv','*.bam']},
    install_requires=[
        'pysam >= v0.15.4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'count_fgs_sam = count_fgs_sam.count_fgs_sam:main',
        ],
    },
    test_suite="count_fgs_sam.tests",
    data_files=[("license", ["LICENSE"])],
)
