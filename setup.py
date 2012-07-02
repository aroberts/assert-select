# -*- coding: utf-8 -*-
"""
assert-select
=============

A convenience library for making assertions about the CSS selectors present
in a rendered template.  Concept lifted directly from Rails.  Code paraphrased
from Rails.

.. _github: http://github.com/aroberts/assert-select
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='assert-select',
    version='0.8',
    url='http://github.com/aroberts/assert-select',
    license='BSD',
    author='Andrew Roberts',
    author_email='adroberts@gmail.com',
    description='Make assertions about CSS selectors',
    long_description=__doc__,
    py_modules=['assert_select'],
    include_package_data=True,
    install_requires=['lxml>=2.3',],
    zip_safe=False,
    platforms='any'
)
