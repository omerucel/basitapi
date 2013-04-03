#-*- coding: utf-8 -*-

import os
from setuptools import setup, find_packages
import basitapi

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name='basitapi',
    version=basitapi.__version__,
    description=read('DESCRIPTION'),
    long_description=read('README.md'),
    license='The MIT LICENCE',
    platforms=['OS Independent'],
    keywords='rest, api, django',
    author='Ömer ÜCEL',
    author_email='omerucel@gmail.com',
    url='https://github.com/omerucel/basitapi',
    packages=find_packages(exclude=['tests', 'cover']),
    include_package_data=True,
    install_requires=[
        'Django',
    ]
)
