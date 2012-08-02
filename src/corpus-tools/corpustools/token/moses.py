# -*- encoding: utf-8 -*-

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
Tokenizer Module for Moses built-in tokenizer
"""

import codecs
import os.path
import sys
from subprocess import call


def tokenize(infile, outfile, lang, tools, step):           # pylint: disable=I0011,W0613
    """Call moses built-in tokenizer for corpus.

    Moses built-in tokenizer support European languages.

    :param infile:        input filename.
    :param outfile:       output filename.
    :param lang:          language of corpus.
    :param tools:         external tools configuration.

    """
    subdir = "tokenizer"
    moses_tokenizer = "tokenizer.perl"
    script = os.path.join(tools["moses.scripts_path"],  subdir, moses_tokenizer)

    in_fp = codecs.open(infile, 'r', 'utf-8')
    out_fp = codecs.open(outfile, 'w', 'utf-8')
    try:
        ret = call([script, "-l", lang], stdin=in_fp, stdout=out_fp)
    except OSError as e:
        print e, ":", script
        sys.exit(e.errno)
    finally:
        in_fp.close()
        out_fp.close()
    return ret
