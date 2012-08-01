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
Regular expression clean module.
"""

import codecs
import re


def run(clean, tools, step):                # pylint: disable=I0011,W0613
    """entry function."""
    ext = step["ext"]
    relist = step["list"]

    compile_relist(relist)

    source_fp = codecs.open(clean.corpus_w(clean.source_lang), 'r', 'utf-8')
    target_fp = codecs.open(clean.corpus_w(clean.target_lang), 'r', 'utf-8')
    source_ext_fp = codecs.open(clean.corpus_w(clean.source_lang, ext), 'w', 'utf-8')
    target_ext_fp = codecs.open(clean.corpus_w(clean.target_lang, ext), 'w', 'utf-8')

    for source_line, target_line in zip(source_fp, target_fp):
        source_line, target_line = relist_clean(source_line, target_line, relist)
        if len(source_line) != 0 and len(target_line) != 0:
            source_ext_fp.write(source_line)
            target_ext_fp.write(target_line)

    source_fp.close()
    target_fp.close()
    source_ext_fp.close()
    target_ext_fp.close()


def compile_relist(relist):
    """Compile the regular expressions to re objects before using them to improve performance.

    :param relist: a list of re clean steps.

    The compiled pattern is assigned back to clean step to replace the string form of pattern.

    """
    for item in relist:
        pattern = item["pattern"]
        flag = 0
        if 'unicode' not in item or item["unicode"] == True:
            flag = flag | re.UNICODE
        if 'case_sensitive' not in item or item["case_sensitive"] == False:
            flag = flag | re.IGNORECASE
        item["pattern"] = re.compile(pattern, flag)

def relist_clean(source, target, relist):
    """Clean source and target sentences with a list of re steps.

    :param source: source corpus sentence.
    :param target: target corpus sentence.
    :param relist: a list of re clean steps.

    :return: (source, target), cleaned corpus align.

    """
    for re_step in relist:
        source = source.strip()
        target = target.strip()
        if len(source) == 0 or len(target) == 0:
            return source, target

        if 'apply_to' in re_step:
            if re_step["apply_to"] == u"source":
                source = re_clean(source, re_step)
            elif re_step["apply_to"] == u"target":
                target = re_clean(target, re_step)
        else:
            source = re_clean(source, re_step)
            target = re_clean(target, re_step)
    return source.strip(), target.strip()

def re_clean(sentence, step):
    """Clean the sentence with clean step, return cleaned corpus sentence.

    :param sentence:  unicode string, corpus sentence.
    :param step:      clean step.

    Example of clean step.

    .. code-block:: bash

        {
          "description": "delete cdata",
          "action": "replace",
          "pattern" : "CDATA",
          "repl" : "",
          "apply_to": "source",
          "unicode": true,
          "case_sensitive": true
        }

    """
    pattern = step["pattern"]
    if step["action"] == "delete_line":
        return re_del(sentence, pattern)
    else:
        if step["action"] == "replace":
            repl = step["repl"]
        elif step["action"] == "delete":
            repl = u''
        return re_repl(sentence, pattern, repl)


def re_del(sentence, pattern):
    """Return empty string if pattern matched.

    :param sentence:  unicode string, corpus sentence.
    :param pattern:   re object.

    """
    return u'' if pattern.search(sentence) else sentence

def re_repl(sentence, pattern, repl):
    """Return substituted sentence.

    :param sentence:  unicode string, corpus sentences.
    :param pattern:   re object.
    :param repl:      unicode string.

    """
    return pattern.sub(repl, sentence)
