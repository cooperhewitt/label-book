#!/usr/bin/env python

from setuptools import setup, find_packages

packages = find_packages()
desc = open("README.md").read(),

setup(
    name='cooperhewitt.label.book',
    namespace_packages=[],
    version='0.14',
    description='Use the Cooper Hewitt API to generate a printable "book" for any exhibition',
    author='Cooper Hewitt, Smithsonian Design Museum',
    url='https://github.com/cooperhewitt/label-book',
    dependency_links=[
        'https://github.com/cooperhewitt/py-cooperhewitt-api/tarball/master#egg=cooperhewitt.api-0.4',
    ],
    install_requires=[
        'cooperhewitt.api',
        'requests'
        ],
    packages=packages,
    download_url='https://github.com/cooperhewitt/label-book/releases',
    license='BSD')