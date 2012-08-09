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

# pylint: disable=I0011,C0301

"""
HTML Clean Module

Unescape the HTML entity (name or codepoint form) to unicode char, remove html
tags.
"""

import codecs
import os
from xml.sax import saxutils
import HTMLParser

def run(clean, tools, step):        # pylint: disable=I0011,W0613
    """entry function."""
    ext = step["ext"]

    for lang in [clean.source_lang, clean.target_lang]:
        unescape(clean.corpus_w(lang), clean.corpus_w(lang, ext))


def unescape(infile, outfile):
    """Unescape xml escape sequences, html entities and tags."""
    infp = codecs.open(infile, 'r', 'utf-8')
    outfp = codecs.open(outfile, 'w', 'utf-8')
    htmlparser = HTMLParser.HTMLParser()

    for line in infile:
        # We need to use saxutils unescape() to convert the &amp; first.
        # use case: &amp;nbsp;
        line = saxutils.unescape(line)
        line = u" ".join(htmlparser.unescape(line).splitlines())
        line = clean_htmltag(line)
        outfp.write(line.strip() + os.linesep)

    infp.close()
    outfp.close()

# TODO: ...
def clean_htmltag(line):
    """clean html tags."""
    return line
