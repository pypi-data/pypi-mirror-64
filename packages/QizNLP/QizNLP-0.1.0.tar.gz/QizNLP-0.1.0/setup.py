#!/usr/bin/env python
# coding: utf-8
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='QizNLP',
    version='0.1.0',
    author='Qznan',
    author_email='summerzynqz@gmail.com',
    description='Quick run NLP in many task',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/Qznan/QizNLP',
    packages=find_packages(),
    package_data={'qiznlp': ['data/*.txt'], },
    install_requires=[
        'jieba',
        'tensorflow>=1.8, <=1.12'
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'qiznlp_init=qiznlp:qiznlp_init',
        ]
    }
)
