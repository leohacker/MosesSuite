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
import re
from xml.sax import saxutils
import HTMLParser

def validate(step):
    return True

def run(clean_config, corpustools_config, step):        # pylint: disable=I0011,W0613
    """entry function."""
    filename = os.path.join(clean_config.working_dir, clean_config.corpus_filename())
    filename_ext = os.path.join(clean_config.working_dir, clean_config.corpus_filename(step["ext"]))

    infp = codecs.open(filename, 'r', 'UTF-8')
    outfp = codecs.open(filename_ext, 'w', 'UTF-8')

    parser = HTMLParser.HTMLParser()

    for line in infp:
        [source, target] = line.split(u'\t')
        source = clean_html(parser, source)
        target = clean_html(parser, target)
        cleanline = u'\t'.join([source, target]) + os.linesep
        outfp.write(cleanline)

    infp.close()
    outfp.close()


def clean_html(parser, line):
    """Unescape xml escape sequences, html entities and clean html tags."""

    # We need to use saxutils unescape() to convert the &amp; first.
    # use case: &amp;nbsp;
    line = saxutils.unescape(line)
    line = u" ".join(parser.unescape(line).splitlines())
    line = clean_htmltag(line)
    return line.strip()


# remove table, form, frame, embedded object.
COMPLEX_TAGS = ['address',
                'applet',
                'button',
                'caption',
                'colgroup',
                'dir',
                'fieldset',
                'form',
                'frameset',
                'iframe',
                'label',
                'legend',
                'map',
                'menu',
                'object',
                'optgroup',
                'option',
                'select',
                'table',
                'tbody',
                'tfoot',
                'thead',
                'th',
                'tr',
                'textarea',
                'ul',
                'ol',
                'dl',
                'noframes',
                'noscript'
]

COMPLEX_SINGLE_TAGS = ['area',
                       'col',
                       'frame',
                       'img',
                       'input',
                       'param'
]

STRUCT_TAGS = ['blockquote',
               'dd',
               'li',
               'p',
               'td'
]

# Keep the content.
INLINE_TAGS = ['a',
               'abbr',
               'acronym',
               'b',
               'bdo',
               'big',
               'cite',
               'center',
               'dfn',
               'em',
               'font',
               'ins',
               'i',
               'q',
               'small',
               'strong',
               'sub',
               'sup',
               'tt',
               'u',
               'var',
               'html',
               'body'
]

# delete the content.
DELETE_TAGS = ['code',
               'del',
               'head',
               'kbd',
               'pre',
               'samp',
               'script',
               'style',
               's',
               'strike',
               'link',
               'title',
               'h1',
               'h2',
               'h3',
               'h4',
               'h5',
               'h6',
               'dt'
]

DELETE_SINGLE_TAGS = ['base',
                      'basefont',
                      'link',
                      'meta',
                      'hr'
]


def clean_htmltag(line):
    """clean html tags."""
    if re.search(ur'<(%s).*?>.*</\1>' % '|'.join(COMPLEX_TAGS), line, re.IGNORECASE):
        return u''
    if re.search(ur'<(%s).*?/>' % '|'.join(COMPLEX_SINGLE_TAGS), line, re.IGNORECASE):
        return u''
    pattern_comment = ur'<!--(.*?)-->'
    pattern_doctype = ur'(?i)<!DOCTYPE.+?>'
    line = re.sub(pattern_comment, ur'\1', line)
    line = re.sub(pattern_doctype, u'', line)

    # <code>...<code >
    for tag in DELETE_TAGS:
        line = re.sub(ur'<(?i){tag}.*?>.*?</{tag} ?>'.format(tag=tag), u'', line)
    for tag in DELETE_SINGLE_TAGS:
        line = re.sub(ur'<(?i){tag}.*?/>'.format(tag=tag), u'', line)

    # <A ...>...<a >
    for tag in INLINE_TAGS:
        line = re.sub(ur'<(?i){tag}.*?>(.*?)</{tag} ?>'.format(tag=tag), ur'\1', line)

    for tag in STRUCT_TAGS:
        line = re.sub(ur'<(?i){tag}.*?>(.*?)</{tag} ?>'.format(tag=tag), ur' \1 ', line)

    # Remove the div and span even they are embedded themselves.
    # The following code works if have correct div/span pairs in sentence.
    # Otherwise some div/span will be left there, maybe not the correct standalone one.
    for tag in ['div', 'span']:
        pattern = ur'<(?i){tag}.*?>(.*?)</{tag} ?>'.format(tag=tag)
        result = re.sub(pattern, ur' \1 ', line, count=1)
        while line != result:
            line = result
            result = re.sub(pattern, ur' \1 ', line, count=1)

    line = re.sub(ur'<br.*?/>', ur' ', line)

    return line
