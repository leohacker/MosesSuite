.. _tmx2txt converter:

******************
TMX2Text Converter
******************

Overview
========
Before feeding the file into moses system for training, we should convert them into plain text first.
TMX2Text Converter(tmx2txt.py) is designed for converting TMX file(s) into plain text files in UTF-8 encoding.

Command line syntax::

    Usage: tmx2txt.py [options] file|directory source_lang target_lang

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o DIR, --output-dir=DIR
                            output directory
      -l FILE, --log=FILE   log file
      -D, --Debug           logging debug message


Module API Documentation
========================

:mod:`tmx2txt` Module
---------------------
.. automodule:: corpustools.tmx2txt
   :members:
   :member-order: bysource


:mod:`format.tmxparser` Module
------------------------------
.. automodule:: corpustools.format.tmxparser
   :members:
   :member-order: bysource