# -*- encoding: utf-8 -*-

# pylint: disable=I0011,C0301,C0103

"""Tokenizer module for Stanford Segmenter."""

import codecs
import os.path
import sys
from subprocess import call
from corpustools.lib.langcode import LangCode


def tokenize(infile, outfile, lang, tools, step):
    """Call Stanford Segmenter for Chinese text.

    Args

        :infile:        input filename.
        :outfile:       output filename.
        :lang:          corpus language.
        :tools:         external tools configuration.
        :step:          tokenizer configuration in step.
    """
    script = os.path.join(tools["stanford_segmenter.path"], 'segment.sh')

    xxlang = LangCode(lang).xx_XX()
    options = step["tool"][xxlang]
    model = options["model"]
    nbest = str(options["nbest"])
    kws = options["keep_whitespace"]

    cmdline = [script, model, infile, "UTF-8", nbest]
    if kws:
        cmdline.insert(1, "-k")

    out_fp = codecs.open(outfile, 'w', 'utf-8')
    try:
        ret = call(cmdline, stdout=out_fp)
    except OSError as e:
        print e, ":", script
        sys.exit(e.errno)
    out_fp.close()

    if ret != 0:
        print "Failed to tokenzie the corpus file:", infile
        sys.exit(ret)
