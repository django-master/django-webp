# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-webp',
    version='1.0.6',
    author=u'Andre Farzat',
    author_email='andrefarzat@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/django-webp/',
    license='MIT',
    description='Returns a webp image instead of jpg, gif or png to browsers which have support',
    long_description=open('README.rst').read(),
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True,
    zip_safe=False,
)
