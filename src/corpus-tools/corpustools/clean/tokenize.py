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

# pylint: disable=I0011,C0301,C0103

"""
Tokenize module in corpus clean tools
"""

import errno
import sys

from corpustools.lib.languagecode import LanguageCode

def tokenize(clean, tools, step, lang):
    """Tokenize the corpus files in corpus clean working directroy.

    Actually, this function works as router to dispatch the request to tokenizers in token subpackage.
    The modules in token subpackage are adapters to external tokenizer tools.

    :param clean:     corpus clean configuration.
    :param tools:     external tools configuration.
    :param step:      clean step.
    :param lang:      specify the language of which corpus be tokenize.

    """
    xxlang = LanguageCode(lang).xx_XX()
    module_name = "corpustools.token." + step["tool"][xxlang]["name"]
    try:
        __import__(module_name)
    except ImportError as e:
        print e
        sys.exit(errno.EPERM)
    module = sys.modules[module_name]
    ret = module.tokenize(clean.corpus_w(lang), clean.corpus_w(lang, step["ext"]), lang, tools, step)
    if ret != 0:
        print "Failed to tokenize file: {0}".format(clean.corpus_w(lang))
        sys.exit(1)


def run(clean, tools, step):
    """Clean module interface function, run tokenization for corpus files."""
    tokenize(clean, tools, step, clean.source_lang)
    tokenize(clean, tools, step, clean.target_lang)
