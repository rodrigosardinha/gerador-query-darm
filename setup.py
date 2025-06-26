#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script para o Processador de DARMs
"""

from setuptools import setup, find_packages
import os

# Ler o README para usar como long_description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Ler requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gerador-query-darm",
    version="1.0.0",
    author="Rodrigo Sardinha",
    author_email="rodrigo.sardinha@example.com",
    description="Sistema automatizado para processamento de DARMs (Documento de Arrecadação de Receitas Municipais)",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/rodrigosardinha/gerador-query-darm",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Filters",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "darm-processor=darm_processor:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.py"],
    },
    keywords="darm, pdf, processamento, receitas, municipais, sql, banco-dados",
    project_urls={
        "Bug Reports": "https://github.com/rodrigosardinha/gerador-query-darm/issues",
        "Source": "https://github.com/rodrigosardinha/gerador-query-darm",
        "Documentation": "https://github.com/rodrigosardinha/gerador-query-darm#readme",
    },
) 