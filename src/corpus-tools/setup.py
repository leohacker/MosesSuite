#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup

setup(name='SMT Corpus Tools',
      version='0.8',
      description='Corpus Tools for SMT',
      author='Leo Jiang',
      author_email='leo.jiang.dev@gmail.com',
      packages=['corpustools',
                'corpustools.case',
                'corpustools.clean',
                'corpustools.config',
                'corpustools.format',
                'corpustools.lib',
                'corpustools.token'],
     )
