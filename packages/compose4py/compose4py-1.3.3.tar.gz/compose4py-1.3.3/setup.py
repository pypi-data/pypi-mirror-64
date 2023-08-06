# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from compose4py import __version__

with open("README.md", "r") as fh:
    long_description = "".join(fh.readlines())

setup(
    name='compose4py',
    version=__version__,
    description='Onion Model in Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Hai Liang Wang',
    author_email='hain@chatopera.com',
    url='https://github.com/chatopera/compose4py',
    license="Apache Software License",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Chinese (Traditional)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities'],
    keywords='onion,compose,chain',
    packages=find_packages(),
    install_requires=[
    ])
