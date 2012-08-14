#!/usr/bin/env python
# -*- coding: utf-8 -*-

# pylint: disable=I0011,C0301

"""
Newline Character Handler Module

Convert the newline characters in the middle of sentence into whitespace. The purpose of opening the file
with default encoding is keeping the newline characters in read line. This ensure we can read the whole line
into a string, then treat this line as utf-8 encoded string. The Unicode version of splitlines() recognize all
kinds of newline characters.

Reference: Unicode TR13: `Unicode Newline Guidelines <http://unicode.org/standard/reports/tr13/tr13-5.html>`_
"""

import codecs
import os
import sys

def run(clean, tools, step):   # pylint: disable=I0011,W0613
    """entry function."""
    for lang in [clean.source_lang, clean.target_lang]:
        normal_newlines(clean.corpus_w(lang), clean.corpus_w(lang, step["ext"]))


def normal_newlines(infile, outfile):
    """delete other newlines except '\n' in the end."""
    # open the infile with ascii encoding to keep other newline characters.
    in_fp = open(infile, 'r')
    out_fp = codecs.open(outfile, 'w', encoding="utf-8")
    for line in in_fp:
        line = ' '.join(unicode(line, 'utf-8').splitlines()).strip()
        out_fp.write(line + os.linesep)
    in_fp.close()
    out_fp.close()

if __name__ == '__main__':
    normal_newlines(sys.argv[1], sys.argv[2])
