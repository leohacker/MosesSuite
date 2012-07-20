#!/usr/bin/env python
# −*− coding: utf−8 −*−

# pylint: disable=C0301,C0111

"""Convert tmx to plain text files.
"""

import sys
from os import path

from optparse import OptionParser
from corpustools.format import TMXParser


def main(argv=sys.argv):    # pylint: disable=W0102
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
