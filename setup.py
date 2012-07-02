# -*- coding: utf-8 -*-
"""
assert-select
========

A convenience library for making assertions about the CSS selectors present
in a rendered template.  Concept lifted directly from Rails.

.. _github: http://github.com/aroberts/assert-select
"""
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name='assert_select',
    version='0.5-dev',
    url='http://github.com/aroberts/assert-select',
    license='BSD',
    author='Andrew Roberts',
    author_email='adroberts@gmail.com',
    description='Make assertions about CSS selectors',
    long_description=__doc__,
    packages=['assert_select',]
    include_package_data=True,
    install_requires=['lxml>=2.3',]
    zip_safe=False,
    platforms='any'
)
