#!/usr/bin/env python
# −*− coding: utf−8 −*−

# License: FreeBSD License or The BSD 2-Clause License

# Copyright (c) year, author
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

"""Convert tmx to plain text files.
"""

import sys
from os import path

from optparse import OptionParser
from corpustools.format.tmxparser import TMXParser


def main(argv=sys.argv):    # pylint: disable=I0011,W0102
    usage = "Usage: %prog [options] tmx_filename source_lang target_lang"
    num_args = 3
    version = "%prog 0.6 (c) 2012 Leo Jiang <leo.jiang.dev@gmail.com>"
    parser = OptionParser(usage=usage, version=version)

    parser.add_option("-o", "--output-dir", metavar="DIR", dest="output_dir",
                      type="string", help="output directory")
    parser.add_option("-l", "--log", metavar="FILE", dest="log",
                      type="string", help="log file")

    (options, args) = parser.parse_args(argv[1:])
    if len(args) != num_args:
        parser.error("Too few/many arguments. Expected {num_args}".format(num_args=num_args))

    filename = path.abspath(path.expanduser(args[1]))
    source_lang = args[2]
    target_lang = args[3]

    parser = TMXParser()
    parser.output_dir = path.abspath(path.expanduser(options.output_dir))
    parser.parse_file(filename, source_lang, target_lang)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
