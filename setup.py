# -*- coding: utf-8 -*-
from distutils.core import setup
from setuptools import find_packages

setup(
    name='django-webp',
    version='0.0.2',
    author=u'Andre Farzat',
    author_email='andrefarzat@gmail.com',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/django-webp/',
    license='LICENSE',
    description='django webp',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').readlines(),
    include_package_data=True,
    zip_safe=False,
)
