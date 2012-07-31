#!/usr/bin/env python
# -*- coding: utf-8 -*-

# License: FreeBSD License or The BSD 2-Clause License

# Copyright (c) 2012, Leo Jiang
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

# Author:   Leo Jiang <leo.jiang.dev@gmail.com>

# pylint: disable=I0011,C0301,C0111

"""
TMX2Text Converter

Convert the tmx file or tmx files in a directory into corpus files. Corpus files
have same basename as tmx file, but suffix with language code.

Command line syntax::

    Usage: tmx2txt.py [options] file|directory source_lang target_lang

    Options:
      --version             show program's version number and exit
      -h, --help            show this help message and exit
      -o DIR, --output-dir=DIR
                            output directory
      -l FILE, --log=FILE   log file
      -D, --Debug           logging debug message

"""

import glob
import logging
import sys
from os import path

from optparse import OptionParser

from corpustools.format.tmxparser import TMXParser
from corpustools.lines import eq_lines, lines

__version__ = 1.0
__years__ = "2012"
__author__ = "Leo Jiang <leo.jiang.dev@gmail.com>"

def main(argv):    # pylint: disable=I0011,W0102
    usage = "Usage: %prog [options] file|directory source_lang target_lang"
    num_args = 3
    version = "%prog {version} (c) {years} {author}".format(version=__version__,
                                                            years=__years__,
                                                            author=__author__
                                                            )
    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-o", "--output-dir", metavar="DIR", dest="output_dir",
                      type="string", help="output directory")
    parser.add_option("-l", "--log", metavar="FILE", dest="log",
                      type="string", help="log file")
    parser.add_option("-D", "--Debug", metavar="DEBUG", dest="debug",
                      action="store_true", help="logging debug message", default="False")
    (options, args) = parser.parse_args(argv[1:])
    if len(args) != num_args:
        parser.error("Too few/many arguments. Expected {num_args}".format(num_args=num_args))

    pathname = path.abspath(path.expanduser(args[0]))
    source_lang = args[1]
    target_lang = args[2]
    if options.output_dir is not None:
        output_dir = path.abspath(path.expanduser(options.output_dir))
    elif path.isdir(pathname):
        output_dir = pathname
    else:
        output_dir = path.dirname(pathname)

    loglevel = logging.INFO
    if options.debug:
        loglevel = logging.DEBUG

    if options.log is not None:
        logging.basicConfig(filename=options.log, level=loglevel, format="%(message)s")
    else:
        logging.basicConfig(level=loglevel, format="%(message)s")

    if path.isdir(pathname):
        for filename in glob.glob(path.join(pathname, "*.tmx")):
            ret = parse_tmx(filename, source_lang, target_lang, output_dir)
            if ret == 0:
                logging.info("Succeed: {0}".format(path.basename(filename)))
            else:
                logging.info("Failed:  {0}".format(path.basename(filename)))
    elif path.isfile(pathname):
        return parse_tmx(pathname, source_lang, target_lang, output_dir)


def parse_tmx(filename, source_lang, target_lang, output_dir):
    """Parse tmx file into corpus files."""
    parser = TMXParser()
    parser.output_dir = output_dir
    ret = parser.parse_file(filename, source_lang, target_lang)
    if ret != 0:
        return 1

    if not eq_lines(parser.source_filepath, parser.target_filepath):
        logging.debug("Failed to parser {0}.".format(filename))
        logging.debug("Lines of {file}: {number}".format(file=parser.source_filepath, number=lines(parser.source_filepath)))
        logging.debug("Lines of {file}: {number}".format(file=parser.target_filepath, number=lines(parser.target_filepath)))
        return 1

    if lines(parser.source_filepath) == 0:
        logging.warning("Warning: empty corpus files.")
    return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
