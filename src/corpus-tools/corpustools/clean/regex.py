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
from itertools import izip
import os
import re

def validate(step):
    return True

def run(clean_config, corpustools_config, step):                # pylint: disable=I0011,W0613
    """entry function."""
    reclean = RegexClean(clean_config, step)
    reclean.run()


class RegexClean(object):
    """Class RegexClean run regular expression clean on source and target corpus."""
    def __init__(self, clean, step):
        self.ext = step["ext"]
        if hasattr(step, "logger"):
            self.logger = step["logger"]
        self.clean = clean
        self.relist = step["list"]
        self.restep = None
        self.lineno = 0

    def run(self):
        """clean the corpus."""
        self.compile_relist()

        filename = os.path.join(self.clean.working_dir, self.clean.corpus_filename())
        filename_ext = os.path.join(self.clean.working_dir, self.clean.corpus_filename(self.ext))

        infp = codecs.open(filename, 'r', 'UTF-8')
        outfp = codecs.open(filename_ext, 'w', 'UTF-8')

        for line in infp:
            self.lineno = self.lineno + 1
            cleanline = self.relist_clean(line)
            outfp.write(cleanline + os.linesep)

        # # Don't use built-in function zip(). Use the iterator version izip() to avoid the MemoryError.
        # for source_line, target_line in izip(source_fp, target_fp):
        #     self.lineno = self.lineno + 1
        #     source_line, target_line = self.relist_clean(source_line, target_line)
        #     if len(source_line) != 0 and len(target_line) != 0:
        #         source_ext_fp.write(source_line + os.linesep)
        #         target_ext_fp.write(target_line + os.linesep)

        infp.close()
        outfp.close()


    def compile_relist(self):
        """Compile the regular expressions to re objects before using them to improve performance.
        The compiled pattern is assigned back to clean step to replace the string form of pattern.

        """
        for item in self.relist:
            pattern = item["pattern"]
            flag = 0
            if 'unicode' not in item or item["unicode"] == True:
                flag = flag | re.UNICODE
            if 'case_sensitive' not in item or item["case_sensitive"] == False:
                flag = flag | re.IGNORECASE
            item["pattern"] = re.compile(pattern, flag)

    def relist_clean(self, line):
        """Clean the line with a list of re steps."""
        [source, target] = line.split(u'\t')

        for re_step in self.relist:
            self.restep = re_step
            source = source.strip()
            target = target.strip()
            if len(source) == 0 or len(target) == 0:
                return u'\t'.join([source, target])

            if 'apply_to' in re_step:
                if re_step["apply_to"] == u"source":
                    source = self.re_clean(source)
                elif re_step["apply_to"] == u"target":
                    target = self.re_clean(target)
            else:
                source = self.re_clean(source)
                target = self.re_clean(target)
        return u'\t'.join([source.strip(), target.strip()])

    def re_clean(self, sentence):
        """Clean the sentence with clean step, return cleaned corpus sentence.

        :param sentence:  unicode string, corpus sentence.

        Example of clean step.

        .. code-block:: bash

            {
              "description": "delete cdata",
              "action": "replace",
              "pattern" : "CDATA",
              "repl" : "",
              "apply_to": "source",
              "unicode": true,
              "case_sensitive": true,
              "log": "detail"
            }

        """
        pattern = self.restep["pattern"]
        if self.restep["action"] == "delete_line":
            return self.re_del(sentence, pattern)
        else:
            if self.restep["action"] == "replace":
                repl = self.restep["repl"]
            elif self.restep["action"] == "delete":
                repl = u''
            return self.re_repl(sentence, pattern, repl)


    def re_del(self, sentence, pattern):
        """Return empty string if pattern matched.

        :param sentence:  unicode string, corpus sentence.
        :param pattern:   re object.
        """
        if pattern.search(sentence):
            if "log" in self.restep:
                if self.restep["log"] == u"detail":
                    self.logger.info(
                        "Line {ln}: Desc={desc}: {match}".format(ln=self.lineno, desc=self.restep["description"],
                                                                 match=pattern.search(sentence).group(0).encode('utf-8'))
                        )
                elif self.restep["log"] == u"lineno":
                    self.logger.info("Line {ln}: Desc={desc}".format(ln=self.lineno, desc=self.restep["description"]))
            return u''
        else:
            return sentence

    def re_repl(self, sentence, pattern, repl):
        """Return substituted sentence.

        :param sentence:  unicode string, corpus sentences.
        :param pattern:   re object.
        :param repl:      unicode string.

        """
        if "log" in self.restep and pattern.search(sentence):
            if  self.restep["log"] == u"detail":
                for match in pattern.finditer(sentence):
                    self.logger.info(
                        "Line {ln}: Desc={desc}: {match}".format(ln=self.lineno, desc=self.restep["description"],
                                                                 match=match.group(0).encode('utf-8'))
                    )
            elif self.restep["log"] == u"lineno":
                self.logger.info("Line {ln}: Desc={desc}".format(ln=self.lineno, desc=self.restep["description"]))

        return pattern.sub(repl, sentence)
