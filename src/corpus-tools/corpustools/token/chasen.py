# -*- encoding: utf-8 -*-

# pylint: disable=I0011,C0301,C0103

"""Tokenizer Module for Japanese Segmenter Chasen."""

import codecs
import os.path
import sys
from subprocess import call


def tokenize(infile, outfile, lang, tools, step):                 # pylint: disable=I0011,W0613
    """Call chasen (Japanese Segmenter) for Japanese text.

    Args

        :infile:        input filename.
        :outfile:       output filename.
        :lang:          language of corpus.
        :tools:         external tools configuration.
    """
    script = os.path.join(tools["chasen.path"], 'chasen')
    rcfile = os.path.join(tools["chasen.path"], 'chasenrc')

    in_fp = codecs.open(infile, 'r', 'utf-8')
    out_fp = codecs.open(outfile, 'w', 'utf-8')
    try:
        ret = call([script, "-r", rcfile, "-i", "w"], stdin=in_fp, stdout=out_fp)
    except OSError as e:
        print e, ":", script
        sys.exit(e.errno)
    in_fp.close()
    out_fp.close()

    if ret != 0:
        print "Failed to tokenize the corpus file:", infile
        sys.exit(ret)
